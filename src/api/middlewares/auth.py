from flask import request, jsonify
import sqlalchemy

from ...models import AuthorizationKey, User
from ...models.User import ADMIN
from ...config.database import  Session
from ..responces import server_error


def check_user_key(function):
    def wrapper(**kwargs):
        try:
            with Session() as session:
                key = request.headers['Authorization-key']
                key_id = request.headers['Authorization-keyId']
                key_db = session.query(AuthorizationKey) \
                    .filter(AuthorizationKey.id == key_id) \
                    .first()
                if key_db:
                    if key_db.key == key:
                        kwargs['key'] = key_db
                        return function(**kwargs)
                    else:
                        return {
                           'error': 'Key is not valid'
                        }, 400
                else:
                    return {
                        'error': 'Unable to find the user authentication key'
                    }, 404
        except Exception as error:
            print(error)
            return server_error.internal_server_error()
    return wrapper


def check_role(role):
    def decorator(function):
        def wrapper(**kwargs):
            try:
                with Session() as session:
                    user_id = kwargs.get('user_id')

                    user = session.execute(
                        sqlalchemy.select(User).where(User.id == user_id)
                    ).scalar_one()

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
            except Exception as e:
                print(e)
                return server_error.internal_server_error()
        return wrapper
    return decorator
