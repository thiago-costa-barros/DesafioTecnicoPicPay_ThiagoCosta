from ninja import Router
from django.db import transaction as dbTransaction
from .models import Entry
from .schemas import EntrySchema
from django.shortcuts import get_object_or_404
from django.http import Http404
from users.models import User
from .validator import isPayerAndPayeeTheSame ,isPayerHasBalance, isPayerHasPermissionToCashOut, isPayeeHasPermissionToCashIn
from django.core.exceptions import ValidationError
from decimal import Decimal
import requests
import json
from core.settings import TESTE_AUTHORIZED_TRANSACTION_ENDPOINT

payments_routers = Router()

@payments_routers.post('/', response={200:dict, 400:dict, 403: dict, 404: dict, 422:dict , 500:dict})

def PaymentsRouter(request, entry: EntrySchema):
    entryValue = Decimal(entry.entryValue).quantize(Decimal("0.00"))
    entryPayerId = entry.payer
    entryPayeeId = entry.payee
    # Payer and Payee Validations
    try:
        try:
            payer = get_object_or_404(User, id=entry.payer)
        except Http404:
            return 404, {  
                'success': 'false',
                'statusCode': 404,
                'message': 'Payer not found. Please check the provided payer ID',
                'payload': {
                    'payerId':entryPayerId
                    }
            }
        try:
            payee = get_object_or_404(User, id=entry.payee)
        except Http404:
            return 404, {  
                'success': 'false',
                'statusCode': 404,
                'message': 'Payee not found. Please check the provided payee ID',
                'payload': {
                    'payeeId':entryPayeeId
                    }
            }
            
        try:
            isPayerAndPayeeTheSame(payer, payee)
        except ValidationError as e:
            return 403, {  
                'success': 'false',
                'statusCode': 403,
                'message': str(e),
                'payload': {
                    'payerId': payer.id,
                    'payeeId': payee.id
                }
            }
    
        # Balance Validation
        try:
            isPayerHasBalance(payer.balance, entryValue)
        except ValidationError as e:
            return 422, {  
                'success': 'false',
                'statusCode': 422,
                'message': str(e),
                'payload': {
                    'payerId': payer.id,
                    'payerBalance':payer.balance,
                    'entryValue': entryValue
                }
            }

        # Permissions roles validations
        try:
            isPayerHasPermissionToCashOut(payer)
        except ValidationError as e:
            return 403, {  
                'success': 'false',
                'statusCode': 403,
                'message': str(e),
                'payload': {
                    'payerId': payer.id,
                    'payerName': payer.username,
                    'payerTaxNumber': payer.taxNumber
                }
            }
            
        try:
            isPayeeHasPermissionToCashIn(payee)
        except ValidationError as e:
            return 403, {  
                'success': 'false',
                'statusCode': 403,
                'message': str(e),
                'payload': {
                    'payerId': payee.id,
                    'payerName': payee.username,
                    'payerTaxNumber': payee.taxNumber
                }
            }
        # Generic Exception
        except Exception as e:
            return 400, {
                'success': 'false',
                'statusCode': 400,
                'message': {
                    'type': 'Generic Error',
                    'error': str(e)
                    },
                'payload': {
                    'entryValue': entryValue,
                    'payerId': entryPayerId,
                    'payeeId': entryPayeeId
                }
            }

        # Sucess True
        with dbTransaction.atomic():
            payer.pay(entry.entryValue)
            payee.receive(entry.entryValue)
            
            
            transactionEntry = Entry(                
                entryValue=entry.entryValue,
                payer=payer,
                payee=payee
            )
            
            payer.save()
            payee.save()
            transactionEntry.save()
            
            getResponseTransactionEntry = requests.get(TESTE_AUTHORIZED_TRANSACTION_ENDPOINT).json()
            if getResponseTransactionEntry.get('status') != 1:
                raise Exception()
        

        return 200, {
            "sucess": True,
            "statusCode": 200,
            "message": "Payment processed",
            "payload": {
                "entryValue": entryValue, 
                "payerId": entryPayerId,
                "payeeId": entryPayeeId
            }
        }
     
    except Exception as e:
        return 500, {
            'success': 'false',
            'statusCode': 500,
            'message': 'Internal server error',
            'error': str(e)
        }
    