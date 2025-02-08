from ninja import Router
from django.db import transaction
from .schemas import EntrySchema

payments_routers = Router()

@payments_routers.post('/', response={200:dict, 400:dict, 422:dict ,500:dict})

def PaymentsRouter(request, entry: EntrySchema):
    print(entry.dict())
    
    return 200, {
        'sucess':'true',
        'statusCode': 200,
        'message': 'Payment processed',
        'payload': {
            'entryValue': entry.entryValue,
            'payerId': entry.payer,
            'payeeId': entry.payee
            }
        }