import json
import tornado.web
import re
import math


def to_reward_points(orderTotal):
    points = int(float(orderTotal))
    return points



def is_email_valid(email):
    reg = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    if re.match(reg, email):
        return True
    else:
        return False
