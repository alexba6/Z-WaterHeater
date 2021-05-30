import datetime
from flask import request
import jwt

from ...config import JWT_KEY, JWT_ALGORITHM
from ...tools.log import logger
from ..middlewares.response import make_json_response


def check_token(function):
    def wrapper(**kwargs):
        try:
            kwargs['token'] = jwt.decode(request.headers['Authorization'], JWT_KEY, JWT_ALGORITHM)
            return function(**kwargs)
        except Exception as error:
            logger.error(error)
            return make_json_response({
                'error': 'Invalid token !'
            }, 498)
    return wrapper


def check_token_date(function):
    def wrapper(**kwargs):
        try:
            current_date = datetime.datetime.now()
            token = kwargs.get('token')
            token_expiration = datetime.datetime.fromisoformat(token['expiration'])
            if current_date > token_expiration:
                raise Exception('Expire token')
            return function(**kwargs)
        except Exception as error:
            logger.error(error)
            return make_json_response({
                'error': 'Expired token !'
            }, 498)
    return wrapper
