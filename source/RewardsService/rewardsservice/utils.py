import re


def email_is_valid(email):
    """Validates email format

    :param email: string
    :return: bool
    """
    regex = r'^[a-z0-9]+[\._-]?[a-z0-9]+[@]\w+[.]\w+$'
    if re.search(regex, email):
        return True
    return False


def total_is_valid(order_total):
    """Validates order total

    :param order_total: string
    :return: bool
    """
    try:
        total = float(order_total)
        if total > 0:
            return True
        return False
    except ValueError:
        return False
