from flask import jsonify
from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError

from ..middlewares.authentification import AuthorizationKeyError, AuthorizationPermissionError

from ..app import app


@app.errorhandler(ValidationError)
def jsonValidatorError(e: ValidationError):
    return jsonify({
        'error': e.validator,
        'path': [path for path in e.path],
        'validatorValue': e.validator_value
    }), 406


@app.errorhandler(JSONDecodeError)
def jsonDecodeError(e: JSONDecodeError):
    return jsonify({
        'error': 'Invalid json !',
        'col': e.colno
    }), 406


@app.errorhandler(AuthorizationKeyError)
def authKeyError(e: AuthorizationKeyError):
    return jsonify({
        'error': e.error,
    }), 401


@app.errorhandler(AuthorizationPermissionError)
def userPermissionError(e: AuthorizationPermissionError):
    return jsonify({
        'error': e.error
    }), 401
