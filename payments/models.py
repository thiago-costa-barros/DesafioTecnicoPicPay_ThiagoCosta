from django.db import models
from users.models import User
from decimal import Decimal

class Entry(models.Model):
    entryValue = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='payerUser', editable=False)
    payee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='payeeUser', editable=False)
    creationDate = models.DateTimeField(auto_created=True, editable=False)
    entryDate = models.DateTimeField(default=None, null=True)
    wasConsolidated = models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return f'From: {self.payer.first_name} | To: {self.payee.first_name} | R$ {self.entryValue} | Data: {self.entryDate}'
