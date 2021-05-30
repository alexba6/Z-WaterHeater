from sqlalchemy import or_
from flask import jsonify

from ....models.User import READER, WRITER, ADMIN, User
from ....config.database import Session
from ...middlewares import auth, format_body, token, response
from ...responces import server_error
from ....tools.log import logger


def user_created_response(user):
    return jsonify({
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role
        }
    }), 201


@response.format_json
@format_body.body_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.check_body(['email', 'username', 'password', 'role'])
def add_user_ctrl(**data):
    try:
        body = data.get('body')
        session = Session()
        find_user = session.query(User) \
            .filter(or_(User.email == body['email'])) \
            .first()
        if find_user:
            return jsonify({
               'error': 'Email already taken !'
            }), 400
        if body['role'] != READER and body['role'] != WRITER:
            return jsonify({
               'error': 'Invalid role !'
            }), 400
        user = User(
            body['email'],
            body['username'],
            body['password'],
            'R'
        )
        session.add(user)
        session.commit()
        return user_created_response(user)
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


@response.format_json
@format_body.body_json
@token.check_token
@token.check_token_date
@format_body.check_body(['email', 'username', 'password'])
def add_user_admin_ctrl(**data):
    try:
        body = data.get('body')
        session = Session()
        user = session.query(User) \
            .filter(User.role == 'A') \
            .first()
        if not user:
            user = User(
                body['email'],
                body['username'],
                body['password'],
                ADMIN
            )
            session.add(user)
            session.commit()
            return user_created_response(user)
        else:
            return jsonify({
                'error': 'Admin user already registered !'
            }), 400

    except Exception as error:
        logger.error(error)
    return server_error.internal_server_error()
