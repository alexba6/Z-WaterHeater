from flask import request
import datetime

from Z_WH.api.middlewares import response, schema
from Z_WH.models import User, AuthorizationKey
from Z_WH.config.database import Session


@response.json
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'login': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    },
    'required': ['login', 'password']
})
def loginCtrl(**kwargs):
    json = kwargs.get('json')
    with Session() as session:
        user = session.query(User) \
            .filter(User.email == json['login']) \
            .first()
        if user:
            if user.verify_password(json['password']):
                date = datetime.datetime.now()
                user.last_login = date
                session.add(user)

                authorization_key = AuthorizationKey()
                authorization_key.user_id = user.id
                authorization_key.user_agent = request.user_agent.string
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
                    'error': 'BAD_PASSWORD'
                }, 401
        else:
            return {
                'error': 'BAD_LOGIN'
            }, 401
