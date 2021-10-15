import re

class validator:
    
    #regular expression found on internet. Check if python has an API for support
    def validateEmail(self, email_address):
        # pass the regular expression
        # and the string into the fullmatch() method    
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email_address)):
            return True
        else:
            return False