from jsonschema.exceptions import ValidationError
from json.decoder import JSONDecodeError

from Z_WH.api.middlewares.authentification import AuthorizationTokenError
from Z_WH.api.middlewares.response import json

from Z_WH.services.verificationCodeManager import VerificationCodeError
from Z_WH.services.autoTimeSlot import AutoTimeSlotManagerError
from Z_WH.services.output import GroupManagerError
from Z_WH.services.user import UserManagerError
from Z_WH.tools.log import Logger


from Z_WH.api.app import app

logger = Logger('api-error')


@json
@app.errorhandler(ValidationError)
def jsonValidatorError(e: ValidationError):
    logger.error(f"ValidationError {e.validator}")
    return {
        'error': e.validator,
        'path': [path for path in e.path],
        'validatorValue': e.validator_value
    }, 406


@json
@app.errorhandler(JSONDecodeError)
def jsonDecodeError(e: JSONDecodeError):
    logger.error("JSONDecodeError")
    return {
        'error': 'Invalid json !',
        'col': e.colno
    }, 406


@json
@app.errorhandler(UserManagerError)
def authKeyError(e: UserManagerError):
    logger.error(f"UserManagerError {e.message}")
    return {
        'error': e.message,
    }, 401


@json
@app.errorhandler(VerificationCodeError)
def verificationCodeError(e: VerificationCodeError):
    logger.error(f"VerificationCodeError {e.status}")
    return {
        'error': e.status
    }, 400


@json
@app.errorhandler(AuthorizationTokenError)
def verificationCodeError(e: AuthorizationTokenError):
    logger.error(f"AuthorizationTokenError {e.message}")
    return {
        'error': e.error
    }, 498


@json
@app.errorhandler(AutoTimeSlotManagerError)
def autoTimeSlotError(e: AutoTimeSlotManagerError):
    logger.error(f"AutoTimeSlotManagerError {e.message}")
    return {
        'error': e.message,
        'slotsId': [slot.id for slot in e.timeSlot]
    }, 400


@json
@app.errorhandler(GroupManagerError)
def groupManagerError(e: GroupManagerError):
    logger.error(f"GroupManagerError {e.message}")
    return {
        'error': e.message
    }, 400
