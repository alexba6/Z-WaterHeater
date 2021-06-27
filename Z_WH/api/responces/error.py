from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError

from Z_WH.api.middlewares.authentification import (
    AuthorizationKeyError, AuthorizationPermissionError, AuthorizationTokenError
)

from Z_WH.api.middlewares.response import json

from Z_WH.services.verificationCodeManager import VerificationCodeError

from Z_WH.api.app import app


@json
@app.errorhandler(ValidationError)
def jsonValidatorError(e: ValidationError):
    return {
        'error': e.validator,
        'path': [path for path in e.path],
        'validatorValue': e.validator_value
    }, 406


@json
@app.errorhandler(JSONDecodeError)
def jsonDecodeError(e: JSONDecodeError):
    return {
        'error': 'Invalid json !',
        'col': e.colno
    }, 406


@json
@app.errorhandler(AuthorizationKeyError)
def authKeyError(e: AuthorizationKeyError):
    return {
        'error': e.error,
    }, 401


@json
@app.errorhandler(AuthorizationPermissionError)
def userPermissionError(e: AuthorizationPermissionError):
    return {
        'error': e.error
    }, 401


@json
@app.errorhandler(VerificationCodeError)
def verificationCodeError(e: VerificationCodeError):
    return {
        'error': e.status
    }, 400


@json
@app.errorhandler(AuthorizationTokenError)
def verificationCodeError(e: AuthorizationTokenError):
    return {
        'error': e.error
    }, 498
