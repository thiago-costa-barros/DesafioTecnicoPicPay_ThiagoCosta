from ninja import Router

users_routers = Router()

@users_routers.post('/', response={200:dict})
def UsersRouter(request):
    return {'Sucess':'true'}