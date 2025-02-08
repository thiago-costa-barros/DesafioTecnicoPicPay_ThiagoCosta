from ninja import Router
from django.db import transaction
from .schemas import TypeUserSchema
from .models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rolepermissions.exceptions import RoleDoesNotExist
from rolepermissions.roles import assign_role
 

users_routers = Router()

@users_routers.post('/', response={200:dict, 400:dict, 422:dict ,500:dict})


def UsersRouter(request, typeUser: TypeUserSchema):
    user = User(**typeUser.user.dict())
    user.password = make_password(typeUser.user.password)
    
    try:
        with transaction.atomic():  
            user.full_clean()  
            user.save()  

            user.groups.clear()  
            assign_role(user, typeUser.typeUser.type)  
            
    except ValidationError as e:
        return 400, {
            'Sucess':'false',
            'StatusCode': 400,
            'Message': {
                'type': 'Bad Request',
                'errors': e.message_dict
            }
        }
    except RoleDoesNotExist as e: 
        return 422, {  
            'Success': 'false',
            'StatusCode': 422,
            'Message': {
                'type': 'Unprocessable Entity',
                'hint': 'The provided role does not exist.'
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
            'balance': user.balance,
            'type': typeUser.typeUser.type
        }
    }