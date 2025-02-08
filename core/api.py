from  ninja import NinjaAPI
from users.api import users_routers
from payments.api import payments_routers

api = NinjaAPI()
api.add_router('users/', users_routers)
api.add_router('payments/',payments_routers)