from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def versioned(path):
    """
    Returns a path to an asset with a version (derived
    from the short hash of the current git commit) in the
    query string.
    
        Sample use:
            {% load assets %}
            <script src="{% versioned '/static/js/main.js' %}"></script>

        Output:
            <script src="/static/js/main.js?v=f498dd2"></script>
    
    Allows far-future expire headers with automatic
    invalidation on code deploys.
    
    See below for required addition to settings.py.
    
    Prior Art: Matt Langer (http://blog.mattlanger.com/post/3200453164)
    """
    return '%s?v=%s' % (path, settings.ASSET_HASH)

# In settings.py...
# Assumes a SITE_ROOT variable as project directory & a git repository
# 
# import subprocess
# 
# ASSET_HASH = subprocess.Popen(
#     "git rev-parse --short HEAD",
#     cwd=SITE_ROOT,
#     stdout=subprocess.PIPE,
#     shell = True).communicate()[0][:-1]