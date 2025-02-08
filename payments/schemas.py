from ninja import ModelSchema
from decimal import Decimal
from .models import Entry

class EntrySchema(ModelSchema):
    
    entryValue: float = Decimal('0.00')
    payer: int  
    payee: int
    
    class Meta:
        model = Entry
        fields = [
            'entryValue',
            'payer',
            'payee'
            ]