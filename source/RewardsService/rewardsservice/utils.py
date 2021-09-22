import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def validate_customer_data(data):
    errors = dict()
    email = data.get("email")
    total = data.get("order_total")
    if not (re.fullmatch(regex, email)):
        errors["email"] = "Enter valid email address"
    try:
        float(total)
    except:
        errors["order_total"] = "Enter valid total amount"
    return errors
