from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime

from ... import validators

class MinMaxValidatorTest(TestCase):
    def test_success(self):
        name = 'example'
        max_value = 1000
        min_value = 50

        value = 200

        validated = validators.min_max_validator(name, max_value, min_value)(value)

        self.assertEqual(validated, value)

    def test_fail(self):
        name = 'example'
        max_value = 1000
        min_value = 50

        value1 = 20
        value2 = 5000

        with self.assertRaises(ValidationError):
            validated = validators.min_max_validator(name, min_value=min_value)(value1)
        
        with self.assertRaises(ValidationError):
            validated = validators.min_max_validator(name, max_value=max_value)(value2)

class AvaValidatorTest(TestCase):
    def test_success(self):
        class obj:
            def __init__(self, width, heigth):
                self.width = width
                self.height = heigth
        
        value = obj(250, 250)

        validated = validators.ava_validator(value)

        self.assertEqual(validated, value)

    def test_fail(self):
        class obj:
            def __init__(self, width, heigth):
                self.width = width
                self.height = heigth
        
        value = obj(50, 700)

        with self.assertRaises(ValidationError):
            validated = validators.ava_validator(value)


class ExpDateValidatorTest(TestCase):
    def test_success(self):
        value = datetime(2020, 1, 1)

        validated = validators.exp_date_validator(value)

        self.assertEqual(validated, value)

    def test_fail(self):
        value = datetime(2019, 1, 1)

        with self.assertRaises(ValidationError):
            validated = validators.exp_date_validator(value)