from django.test import TestCase
from django.core.exceptions import ValidationError

from ... import validators

# Done!
class RegexValidatorTest(TestCase):
    def test_success(self):
        name = 'Phone number'
        regex = '[0-9]\-?[0-9]{2}\-?[0-9]{2}'
        value = '2-9234'

        validated = validators.regex_validator(name, regex)(value)

        self.assertEqual(validated, value)

    def test_fail(self):
        name = 'Phone number'
        regex = '[0-9]\-?[0-9]{2}\-?[0-9]{2}'
        value = '2-923-456'

        with self.assertRaises(ValidationError):
            validated = validators.regex_validator(name, regex)(value)

# Done!
class AbbrValidatorTest(TestCase):
    def test_success(self):
        value = 'pony'

        validated = validators.abbr_validator(value)

        self.assertEqual(validated, value)

    def test_fail(self):
        value = 'a12'

        with self.assertRaises(ValidationError):
            validated = validators.abbr_validator(value)

# Done!
class CSVValidatorTest(TestCase):
    def test_success(self):
        value = 'example,sage'

        validated = validators.csv_validator(value)

        self.assertEqual(validated, value)

    def test_fail(self):
        value1 = 'example,'
        value2 = ',example'

        with self.assertRaises(ValidationError):
            validated = validators.csv_validator(value1)

        with self.assertRaises(ValidationError):
            validated = validators.csv_validator(value2)