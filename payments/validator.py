from django.core.exceptions import ValidationError
from rolepermissions.checkers import has_permission

def isPayerAndPayeeTheSame(payer, payee):
    if payer == payee:
        raise ValidationError("Payer and payee cannot be the same.")
    return True

def isPayerHasBalance(payer_balance, entryValue):
    if payer_balance < entryValue:
        raise ValidationError("Payer does not have enough balance to this transaction.")
    return True

def isPayerHasPermissionToCashOut(payer):
    if not has_permission(payer, 'cash_out'):
        raise ValidationError("Payer does not have permission to make this transaction.")
    return True

def isPayeeHasPermissionToCashIn(payer):
    if not has_permission(payer, 'cash_in'):
        raise ValidationError("Payee does not have permission to receive this transaction.")
    return True