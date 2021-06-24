from flask import request

from ...models.User import WRITER, ADMIN, User
from ...models.AuthorizationKey import AuthorizationKey
from ...config.database import Session


class AuthorizationKeyError(Exception):
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
                user = session.query(User) \
                    .filter(User.id == keyDb.user_id) \
                    .first()
                if user is None:
                    raise AuthorizationPermissionError('INVALID_USER')
                if user.role != role or user.role != ADMIN:
                    raise AuthorizationPermissionError('INVALID_ROLE')
                kwargs['userId'] = user.id
                return func(*arg, **kwargs)
        return inner
    return wrapper
