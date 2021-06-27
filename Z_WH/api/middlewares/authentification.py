import datetime
from flask import request
from jwt import decode, encode, PyJWTError

from Z_WH.models.User import WRITER, ADMIN, User
from Z_WH.models.AuthorizationKey import AuthorizationKey
from Z_WH.config.database import Session
from Z_WH.config.jwt import JWT_KEY, JWT_ALGORITHM


class AuthorizationKeyError(Exception):
    def __init__(self, error: str, message: str = None):
        self.error: str = error
        self.message: str = message


class AuthorizationTokenError(Exception):
    def __init__(self, error: str, message: str = None):
        self.error: str = error
        self.message: str = message


class AuthorizationPermissionError(Exception):
    def __init__(self, error: str, message: str = None):
        self.error: str = error
        self.message: str = message


def checkUserKey(role=WRITER):
    def wrapper(func):
        def inner(*arg, **kwargs):
            key = request.headers.get('Authorization-key')
            keyId = request.headers.get('Authorization-keyId')
            if key is None or keyId is None:
                raise AuthorizationKeyError(
                    'KEY_KEYID_EMPTY_HEADER',
                    'Key and keyId headers cannot be empty !'
                )
            with Session() as session:
                keyDb: AuthorizationKey = session.query(AuthorizationKey) \
                    .filter(AuthorizationKey.id == keyId) \
                    .first()
                if keyDb is None:
                    raise AuthorizationKeyError(
                        'INVALID_KEY',
                        'Cannot find the key !'
                    )
                if keyDb.key != key:
                    raise AuthorizationKeyError(
                        'INVALID_KEY',
                        'Invalid key !'
                    )
                kwargs['keyId'] = keyDb.id
                user = session.query(User) \
                    .filter(User.id == keyDb.user_id) \
                    .first()
                if user is None:
                    raise AuthorizationPermissionError('INVALID_USER')
                if user.role != role and user.role != ADMIN:
                    raise AuthorizationPermissionError('INVALID_ROLE')
                kwargs['userId'] = user.id
                return func(*arg, **kwargs)
        return inner
    return wrapper


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
