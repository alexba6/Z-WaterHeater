import datetime
import jwt

from ....config import JWT_ALGORITHM, JWT_KEY
from ....services.verificationCode import verificationCode, VerificationCodeError
from ...middlewares import format_body, response


@response.json
def generate_code_ctrl():
    try:
        valid_time = 6
        verificationCode.generateCode(60)
        return {
            'message': 'Code generated !',
            'validTime': valid_time
        }, 200
    except VerificationCodeError as e:
        return {
           'error': e.status
        }, 400


@response.json
@format_body.body_json
@format_body.check_body(['code'])
def check_code(body):
    try:
        verificationCode.verifyCode(body['code'])
        valid_time = 60*20
        token = jwt.encode({
            'expiration': (datetime.datetime.now() + datetime.timedelta(seconds=valid_time)).isoformat()
        }, JWT_KEY, JWT_ALGORITHM)
        return {
            'message': 'Verification ok',
            'token': token,
            'validTime': valid_time
        }, 200
    except VerificationCodeError as error:
        return {
           'error': error.status
        }, 400
