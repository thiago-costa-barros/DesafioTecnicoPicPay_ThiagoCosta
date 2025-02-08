from ninja import ModelSchema, Schema
from .models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'taxNumber',
            'password'
            ]
        
class TypeSchema(Schema):
    type: str
    
class TypeUserSchema(Schema):
    user: UserSchema
    typeUser: TypeSchema