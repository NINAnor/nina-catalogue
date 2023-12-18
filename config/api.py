from ninja import NinjaAPI

from metadata_catalogue.maps.api import maps_router

api = NinjaAPI()

api.add_router("/maps/", maps_router)
