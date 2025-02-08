import re
from django.core.exceptions import ValidationError

def isTaxNumberValid(taxNumber):
    """ If cnpf in the Brazilian format is valid, it returns True, otherwise, it returns False. """

    # Check if type is str
    if not isinstance(taxNumber,str):
        raise ValidationError('TaxNumber must be a string')

    # Remove some unwanted characters
    taxNumber = re.sub("[^0-9]",'',taxNumber)

    # Checks if string has 11 characters
    if len(taxNumber) != 11:
        raise ValidationError('TaxNumber must have 11 characters')

    # Check if all digits are equal
    if (taxNumber == taxNumber[0] * 11):
        raise ValidationError('TaxNumber is not valid')
    
    # Checks if string has 11 characters
    if len(taxNumber) != 11:
        raise ValidationError('TaxNumber must have 11 characters')
    
    sum = 0
    weight = 10

    """ Calculating the first taxNumber check digit. """
    for n in range(9):
        sum = sum + int(taxNumber[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    """ Calculating the second check digit of taxNumber. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(taxNumber[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifyingDigit = 11 -  sum % 11

    if verifyingDigit > 9 :
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if taxNumber[-2:] == "%s%s" % (firstVerifyingDigit,secondVerifyingDigit):
        return True
    raise ValidationError('TaxNumber is not valid')