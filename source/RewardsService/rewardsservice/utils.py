import re 
  
# Make a regular expression 
# for validating an Email 
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

# Define a function for 
# for validating an Email 
def is_email_valid(email):

    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):
        return True
    else:
        return False