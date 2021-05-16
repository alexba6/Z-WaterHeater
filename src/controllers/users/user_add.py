from flask import request
from sqlalchemy import or_
from ...models import User
from ...config.database import Session
from ...config import DEBUG
from ...responces import server_error
from ...middlewares import extract_request


@extract_request.body_json(request)
@extract_request.check_body(['email', 'username', 'password'])
def add_user_ctrl(body):
    print()
    try:
        session = Session()
        find_user = session.query(User) \
            .filter(or_(User.email == body['email'])) \
            .first()
        if find_user:
            return {
               'error': 'Email already taken !'
            }, 400
        user = User(**body)
        session.add(user)
        session.commit()
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role
            }
        }, 201
    except Exception as error:
        if DEBUG:
            print(error)
        return server_error.internal_server_error()
