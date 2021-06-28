import random


def getRandomString(charts: str, length: int):
    return ''.join(map(lambda i: random.choice(charts), range(length)))
