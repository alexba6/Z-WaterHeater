from flask import request, jsonify

from src.models import AuthorizationKey, User
from src.models.User import ADMIN
from src.config.database import Session
from src.http.responces import server_error


def check_user_key(function):
    def wrapper(**kwargs):
        try:
            session = Session()
            key = request.headers['Authorization-key']
            key_id = request.headers['Authorization-keyId']
            key_db = session.query(AuthorizationKey) \
                .filter(AuthorizationKey.id == key_id) \
                .first()
            if key_db:
                if key_db.key == key:
                    kwargs['user_id'] = key_db.user_id
                    return function(**kwargs)
                else:
                    return jsonify({
                       'error': 'Key is not valid'
                    }), 400
            else:
                return jsonify({
                    'error': 'Unable to find the user authentication key'
                }), 404
        except Exception as error:
            print(error)
            return server_error.internal_server_error()
    return wrapper


def check_role(role):
    def decorator(function):
        def wrapper(**kwargs):
            try:
                session = Session()
                user_id = kwargs.get('user_id')
                user = session.query(User) \
                    .filter(User.id == user_id) \
                    .first()
                if user:
                    if user.role == role or user.role == ADMIN:
                        return function(**kwargs)
                    else:
                        return jsonify({
                            'error': 'Your are not allowed !'
                        }), 400
                else:
                    return jsonify({
                        'error': 'User not found !'
                    }), 400
            except:
                return server_error.internal_server_error()
            return
        return wrapper
    return decorator
