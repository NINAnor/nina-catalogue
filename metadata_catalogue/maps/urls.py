from ninja import NinjaAPI

from .apis import maps_router

api = NinjaAPI()
api.add_router("/maps/", maps_router)
