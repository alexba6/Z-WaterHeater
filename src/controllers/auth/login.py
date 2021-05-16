from flask import request
import datetime
from ...middlewares import extract_request
from ...responces import server_error
from ...models import User, AuthorizationKey
from ...config.database import Session
from ...config import DEBUG


@extract_request.body_json(request)
@extract_request.check_body(['login', 'password'])
def login_ctrl(body):
    try:
        session = Session()
        user = session.query(User) \
            .filter(User.email == body['login']) \
            .first()

        if user:
            if user.verify_password(body['password']):
                date = datetime.datetime.now()
                authorization_key = AuthorizationKey()
                authorization_key.user_id = user.id
                authorization_key.user_agent = request.user_agent
                authorization_key.created_at = date
                authorization_key.last_generated = date
                key = authorization_key.generate_key()
                session.add(authorization_key)
                session.commit()

                return {
                   'key_id': authorization_key.id,
                   'key': key
                }, 200

            else:
                return {
                    'error': 'Bad credential !'
                }, 400
        else:
            return {
               'error': 'User not found !'
            }, 404
    except Exception as error:
        if DEBUG:
            print(error)
        return server_error.internal_server_error()
