from rolepermissions.roles import AbstractUserRole

class People(AbstractUserRole):
    available_permissions = {
        'cash_out': True,
        'cash_in': True,
    }
    
class Company(AbstractUserRole):
    available_permissions = {
        'cash_out': False,
        'cash_in': True,
    }