from flask import request
import datetime

from ...middlewares import format_body, response
from ...responces import server_error
from ....models import User, AuthorizationKey
from ....config.database import Session
from ....tools.log import logger


@response.format_json
@format_body.body_json
@format_body.check_body(['login', 'password'])
def login_ctrl(**data):
    try:
        body = data.get('body')
        session = Session()
        user = session.query(User) \
            .filter(User.email == body['login']) \
            .first()
        if user:
            if user.verify_password(body['password']):
                date = datetime.datetime.now()

                user.last_login = date
                session.add(user)

                authorization_key = AuthorizationKey()
                authorization_key.user_id = user.id
                authorization_key.user_agent = request.user_agent
                authorization_key.created_at = date
                authorization_key.last_generated = date
                key = authorization_key.generate_key()

                session.add(authorization_key)

                session.commit()

                return {
                    'keyId': authorization_key.id,
                    'key': key
                }, 200

            else:
                return {
                    'error': 'BAD_CREDENTIALS'
                }, 401
        else:
            return {
                'error': 'BAD_CREDENTIALS'
            }, 401
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()
