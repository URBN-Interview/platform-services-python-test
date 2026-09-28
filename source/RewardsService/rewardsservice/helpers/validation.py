import json
import re

class ValidationError(ValueError):
    pass

def validate_email(email_value):
    if not isinstance(email_value, str):
        raise ValidationError("email must be a string")
    email = email_value.strip().lower()
    if not re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$").fullmatch(email):
        raise ValidationError("email must be valid")
    return email

def validate_order_total(value):
    if not isinstance(value, (int, float)):
        raise ValidationError("order_total must be a number")
    if value <= 0:
        raise ValidationError("order_total must be positive")
    return value

def parse_order_body(body):
    try:
        data = json.loads(body)
    except ValueError:
        raise ValidationError("request body must be valid JSON")
    if not isinstance(data, dict):
        raise ValidationError("request body must be a JSON object")
    if "email_address" not in data:
        raise ValidationError("email is required")
    if "order_total" not in data:
        raise ValidationError("order_total is required")
    return validate_email(data["email_address"]), validate_order_total(data["order_total"])
