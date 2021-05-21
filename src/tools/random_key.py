import string
import random


def generate_key(length=250, charts=string.ascii_uppercase + string.ascii_lowercase + string.digits + '-'):
    return ''.join(random.choice(charts) for i in range(length))
