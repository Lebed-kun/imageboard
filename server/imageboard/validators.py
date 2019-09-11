import re

from django.core.exceptions import ValidationError

ABBR_REGEX = '[a-z]+'
CSV_REGEX = '(\w+\,)+\w+'

def regex_validator(regex, name=None):
    def validator(value):
        match = re.match(regex, value)

        if not match:
            name = name if name is not None else 'value'
            raise ValidationError('Invalid ' + name)
        else:
            return value
    return validator

abbr_validator = lambda value : regex_validator(ABBR_REGEX, 'uri of board')(value)
csv_validator = lambda value : regex_validator(CSV_REGEX, 'list')(value)
