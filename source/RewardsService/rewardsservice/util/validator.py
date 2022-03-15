import re
from util.server_error import ValidationError

emailRegex  = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
currencyRegex = '^\d+(\.|\,)\d{2}$'


class Validator:

    def __init__(self):
        self.errors = list()

    def _validator(self, regex, email, regrexType, name):
        isValid = True
        result = re.fullmatch(regex, email)
        if not result:
            isValid = False
        return isValid

    def validate(self):
        if len(self.errors) > 0:
            error = ValidationError(self.errors)
            return error

    def emailValidation(self, email, name):
        return self._validator(emailRegex, email, 'email', name)

    def currencyValidation(self, currency, name):
        return self._validator(currencyRegex, currency, 'currency', name)
