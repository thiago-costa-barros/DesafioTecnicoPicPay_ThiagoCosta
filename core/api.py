from  ninja import NinjaAPI
from users.api import users_routers

api = NinjaAPI()
api.add_router('users/', users_routers)