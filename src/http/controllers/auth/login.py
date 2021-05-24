from flask import request, jsonify
import datetime
from src.http.middlewares import format_body
from src.http.responces import server_error
from src.models import User, AuthorizationKey
from src.config.database import Session
from src.config import DEBUG


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

                return jsonify({
                    'key_id': authorization_key.id,
                    'key': key
                }), 200

            else:
                return jsonify({
                    'error': 'Bad credential !'
                }), 401
        else:
            return jsonify({
                'error': 'Bad credential !'
            }), 401
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()
