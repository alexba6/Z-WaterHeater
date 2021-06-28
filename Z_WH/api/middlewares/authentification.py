import datetime
from flask import request
from jwt import decode, encode, PyJWTError

from Z_WH.config.jwt import JWT_KEY, JWT_ALGORITHM

from Z_WH.services import userManager
from Z_WH.services.user import UserManagerError



class AuthorizationTokenError(Exception):
    def __init__(self, error: str, message: str = None):
        self.error: str = error
        self.message: str = message


class AuthorizationPermissionError(Exception):
    def __init__(self, error: str, message: str = None):
        self.error: str = error
        self.message: str = message


def checkUserKey(func):
    def inner(*arg, **kwargs):
        key = request.headers.get('Authorization-key')
        keyId = request.headers.get('Authorization-keyId')
        userManager.checkKey(keyId, key)
        kwargs['keyId'] = keyId
        return func(*arg, **kwargs)
    return inner


def checkUserToken(func):
    def inner(*arg, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthorizationTokenError('TOKEN_NOT_FOUND')
        payload = None
        try:
            payload = decode(token, JWT_KEY, JWT_ALGORITHM)
        except PyJWTError as error:
            print(error)

        now = datetime.datetime.now()
        if payload is None:
            raise AuthorizationTokenError('INVALID_TOKEN')
        expiration = payload.get('expiration')
        if expiration is None:
            raise AuthorizationTokenError('INVALID_TOKEN')
        tokenExpiration = datetime.datetime.fromisoformat(expiration)
        if not tokenExpiration:
            raise AuthorizationTokenError('INVALID_TOKEN')
        if now > tokenExpiration:
            raise AuthorizationTokenError('EXPIRED_TOKEN')
        return func(*arg, **kwargs)
    return inner


def createToken(expiration: int, data: object = None) -> bytes:
    return encode({
        'expiration': (datetime.datetime.now() + datetime.timedelta(seconds=expiration)).isoformat(),
        'data': data
    }, JWT_KEY, JWT_ALGORITHM)
