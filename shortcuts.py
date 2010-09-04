from django.shortcuts import render_to_response
from django.template import RequestContext

# Prior art: http://github.com/mintchaos/mint_django_utils/tree/master
def render_with_context(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)
