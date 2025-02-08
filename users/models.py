import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from .validator import isTaxNumberValid

class User(AbstractUser):
    taxNumber = models.CharField(max_length=14, unique=True, validators=[isTaxNumberValid])
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    
    def save(self, *args, **kwargs):
        self.taxNumber = re.sub("[^0-9]", '',self.taxNumber)
        super(User, self).save(*args, **kwargs)
        
    def pay(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError("Value must be a Decimal instance")
        
        self.balance -= value
        
    def receive(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError("Value must be a Decimal instance")
        
        self.balance += value