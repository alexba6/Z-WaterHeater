import datetime
import jwt

from ...responces import server_error
from ...config import DEBUG, JWT_ALGORITHM, JWT_KEY
from ...tools.verification_code import code_generator, VALID_CODE, EXPIRED_CODE, INVALID_CODE
from ...middlewares import format_body


def generate_code_ctrl():
    try:
        if code_generator.code_expire():
            valid_time = 30
            code_generator.start_code(valid_time)
            return {
                'message': 'Code generated !',
                'valid_time': valid_time
            }, 200
        else:
            return {
                'error': 'There is already code !'
            }, 400
    except Exception as error:
        if DEBUG or 1:
            print(error)
    return server_error.internal_server_error()


@format_body.body_json
@format_body.check_body(['code'])
def check_code(body):
    try:
        code = body['code']
        status = code_generator.verify_code(code)
        if status == EXPIRED_CODE:
            return {
                'error': 'Code has expired !'
            }, 400
        elif status == INVALID_CODE:
            return {
                'error': 'Code is not valid !'
            }, 400
        elif status == VALID_CODE:
            valid_time = 60*20
            token = jwt.encode({
                'expiration': (datetime.datetime.now() + datetime.timedelta(seconds=valid_time)).isoformat()
            }, JWT_KEY, JWT_ALGORITHM)
            return {
                'message': 'Verification ok',
                'token': token,
                'valid_time': valid_time
            }, 200
    except Exception as error:
        if DEBUG or 1:
            print(error)
    return server_error.internal_server_error()
