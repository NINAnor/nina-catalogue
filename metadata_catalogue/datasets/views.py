from django.http import HttpResponse, HttpResponseNotFound

from .models import Dataset


def get_dataset_vrt_view(request, dataset_uuid):
    try:
        dataset = Dataset.objects.select_related("content").get(uuid=dataset_uuid)
        content = dataset.content.gdal_vrt_definition.replace("{{SOURCE}}", dataset.content.get_gdal_vrt_source())
        return HttpResponse(content, content_type="text")
    except Dataset.DoesNotExist:
        return HttpResponseNotFound()
