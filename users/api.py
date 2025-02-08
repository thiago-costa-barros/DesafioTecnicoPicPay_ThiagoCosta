from ninja import Router
from .schemas import UserSchema
from .models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError 

users_routers = Router()

@users_routers.post('/', response={200:dict, 400:dict, 500:dict})


def UsersRouter(request, user: UserSchema):
    user = User(**user.dict())
    user.password = make_password(user.password)
    
    try:
        user.full_clean() # Verify validators
        user.save()
    except ValidationError as e:
        return 400, {
            'Sucess':'false',
            'StatusCode': 400,
            'Message': {
                'errors': e.message_dict
            }
        }
    except Exception as e:
        return 500, {
            'Sucess':'false',
            'StatusCode': 500,
            'Message': {
                'type':'Internal Server Error',
                'error': str(e)
            }
        }
    
    return {
        'Sucess':'true',
        'StatusCode': 200,
        'Message': 'User created successfully',
        'Data': {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'taxNumber': user.taxNumber,
            'balance': user.balance
            }
        }