import re

emailRegex  = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
currencyRegex = '^[0-9]+\.[0-9]{2}'

class Validaton:

    def __init__(self):
        self.message = ''
        self.errorExist = False

    def _setMessage(self, message):
        self.message = '%s \n %s' % (self.message, message)

    def _validator(self, regex, data, name):
        result = re.search(regex, data)
        if(not result):
            self._setMessage('Invalid %s validation' % (name))
            self.errorExist = True
        return self

    def validate(self):
        if(self.errorExist):
            raise Exception(self.message)

    def emailValidation(self, email):
        return self._validator(emailRegex, email, 'email')

    def currencyValidation(self, currency):
        return self._validator(currencyRegex, currency, 'currency')

