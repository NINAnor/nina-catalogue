from django.http import HttpResponse, HttpResponseNotFound

from .models import Dataset


def get_dataset_vrt_view(request, dataset_uuid):
    try:
        dataset = Dataset.objects.select_related("content").get(uuid=dataset_uuid)
        return HttpResponse(dataset.content.gdal_vrt_definition, content_type="text")
    except Dataset.DoesNotExist:
        return HttpResponseNotFound()
