from django import template
from django.template.defaultfilters import date as datefilter

register = template.Library()

@register.simple_tag
def timeago(datetime):
    """
    Inserts <abbr> tag that works with timeago js script.
    More info: http://timeago.yarp.com/
    """
    
    html = '<abbr class="timeago" title="{{ISODATE}}">{{PRETTYDATE}}</abbr>'
    iso_date = datetime.isoformat()
    # cut off nasty milliseconds that confuse timeago
    index = iso_date.find('.')
    if index != -1:
        iso_date = iso_date[:index]
    pretty_date = datefilter(datetime, "F j, Y, P")
    return html.replace("{{ISODATE}}", iso_date).replace("{{PRETTYDATE}}", pretty_date)