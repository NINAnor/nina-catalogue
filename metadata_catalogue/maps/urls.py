from ninja import NinjaAPI

from .api import maps_router

api = NinjaAPI()
api.add_router("/maps/", maps_router)
