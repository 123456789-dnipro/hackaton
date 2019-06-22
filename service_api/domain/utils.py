from random import randint
from uuid import uuid4


def generate_uuid():
    return str(uuid4())


def generate_sms():
    return randint(999, 9999)
