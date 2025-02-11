from ninja import ModelSchema
from decimal import Decimal
from .models import Entry

class EntrySchema(ModelSchema):
    
    entryValue: Decimal
    
    class Meta:
        model = Entry
        fields = [
            'entryValue',
            'payer',
            'payee'
            ]