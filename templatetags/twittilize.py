# Copyright (c) 2009 Six Apart Ltd.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of Six Apart Ltd. nor the names of its contributors may
#   be used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import htmlentitydefs
import re
from urllib import quote

from django import template
from django.template.defaultfilters import urlize, stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


def needs_autoescape(fn):
    fn.needs_autoescape = True
    return fn


usernames_re = re.compile(r"""
        (?: (?<= \A @ )    # leading at
          | (?<= \s @ ) )  # or spaced at
        \w+                # and a name
    """, re.VERBOSE | re.MULTILINE | re.DOTALL)


hashtags_re = re.compile(r"""
        (?: (?<= \A )    # beginning of string
          | (?<= \s ) )  # or whitespace
        \#               # the hash
        \w               # the tag, which starts with a word char
        (?: [^\s&]       # contains non-whitespace characters
          | &[^;]+; )*   # and complete character entities
        \w               # and ends with another word char
        (?<! 's )        # but doesn't end with "'s"
        (?<! &\#39;s )   # or an encoded "'s"
    """, re.VERBOSE | re.MULTILINE | re.DOTALL)


html_numeric_entity_re = re.compile(r"""
        &\#
        (\d+)  # some decimal digits
        ;
    """, re.VERBOSE | re.MULTILINE | re.DOTALL)


html_named_entity_re = re.compile(r"""
        &
        (\w+)  # the entity name
        ;
    """, re.VERBOSE | re.MULTILINE | re.DOTALL)


def html_escaped_to_uri_escaped(text):
    text = re.sub(
        html_numeric_entity_re,
        lambda m: unichr(int(m.group(1))),
        text,
    )
    text = re.sub(
        html_named_entity_re,
        lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]),
        text,
    )
    return quote(text)


@register.filter
@needs_autoescape
@stringfilter
def twittilize(tweet, autoescape=None):
    if autoescape:
        tweet = conditional_escape(tweet)

    # Auto-link URLs (using Django's implementation).
    tweet = urlize(tweet)

    # Auto-link Twitter username references.
    tweet = re.sub(
        usernames_re,
        lambda m: '<a href="http://twitter.com/%s">%s</a>' % (m.group(0), m.group(0)),
        tweet,
    )

    # Auto-link hashtags.
    tweet = re.sub(
        hashtags_re,
        lambda m: ('<a href="http://twitter.com/search?q=%s">%s</a>'
            % (html_escaped_to_uri_escaped(m.group(0)), m.group(0))),
        tweet,
    )

    return mark_safe(tweet)
