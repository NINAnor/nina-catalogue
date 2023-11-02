import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pycsw import server

from metadata_catalogue.csw.models import CSWConfig


@csrf_exempt
def csw_invoke(request, *args, **kwargs):
    csw_settings = CSWConfig.get_solo()
    env = request.META.copy()
    env.update(
        {
            "local.app_root": os.path.dirname(__file__),
            "REQUEST_URI": request.build_absolute_uri().replace("%", "%%"),
        }
    )
    csw_conf = csw_settings.get_config(request.build_absolute_uri().replace("%", "%%"))
    csw = server.Csw(csw_conf, env)
    status, content = csw.dispatch_wsgi()
    status_code, _status_message = status.split(" ", 1)
    status_code = int(status_code)
    return HttpResponse(content, content_type=csw.contenttype, status=status_code)
