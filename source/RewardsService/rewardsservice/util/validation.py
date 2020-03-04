import re
from util.server_error import ValidationError

emailRegex  = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
currencyRegex = '^\d+(\.|\,)\d{2}$'

class Validaton:

    def __init__(self):
        self.errors = list()

    def _validator(self, regex, data, regrexType, name):
        result = re.search(regex, data)
        if(not result):
            self.errors.append('%s does not match %s format' %(name, regrexType))
        return self

    def validate(self):
        if len(self.errors) > 0:
            error = ValidationError(self.errors)
            return error

    def emailValidation(self, email, name):
        return self._validator(emailRegex, email, 'email', name)

    def currencyValidation(self, currency, name):
        return self._validator(currencyRegex, currency, 'currency', name)

