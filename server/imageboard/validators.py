import re

from django.core.exceptions import ValidationError

ABBR_REGEX = '[a-z]+'
CSV_REGEX = '(\w+\,)+\w+'

MIN_AVA_SIZE = 100
MAX_AVA_SIZE = 500

# General validators

def regex_validator(name, regex):
    def validator(value):
        match = re.match(regex, value)

        if not match:
            raise ValidationError('Invalid ' + name)
        else:
            return value
    return validator

def min_max_validator(name, max_value=None, min_value=None, compare=(lambda a, b : a - b)):
    def validator(value):
        if max_value is not None and compare(value, max_value) > 0:
            raise ValidationError(name + ' should be at most ' + max_value)
        if min_value is not None and compare(value, min_value) < 0:
            raise ValidationError(name + ' should be at least ' + min_value)

        return value
    return validator

# Actual validators

abbr_validator = lambda value : regex_validator('uri of board', ABBR_REGEX)(value)
csv_validator = lambda value : regex_validator('list', CSV_REGEX)(value)

def ava_validator(value):
    (errors, image_info) = ([], value.info()['image_info'])

    compareWidth = lambda value, border : value['width'] - border
    compareHeight = lambda value, border : value['height'] - border

    width_validator = min_max_validator('width', MAX_AVA_SIZE, MIN_AVA_SIZE, compareWidth)
    height_validator = min_max_validator('height', MAX_AVA_SIZE, MIN_AVA_SIZE, compareHeight) 

    width = width_validator(value)
    height = height_validator(value)

    if width and height:
        return value
