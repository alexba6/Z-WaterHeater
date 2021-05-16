from flask import request
import datetime
from ...models import AuthorizationKey
from ...middlewares import extract_request
from ...responces import server_error
from ...config.database import Session
from ...config import DEBUG


@extract_request.body_json(request)
@extract_request.check_body(['key_id', 'key'])
def regenerate_key_ctrl(body):
    try:
        date = datetime.datetime.now()
        session = Session()
        authorization_key = session.query(AuthorizationKey)\
            .filter(AuthorizationKey.id == body['key_id'])\
            .first()
        if authorization_key:
            if authorization_key.match_key(body['key']):
                authorization_key.last_generated = date
                key = authorization_key.generate_key()
                session.commit()
                return {
                    'key_id': authorization_key.id,
                    'new_key': key
                }, 200
            else:
                return {
                    'error': 'Invalid authorization key !'
                }, 400
        else:
            return {
                'error': 'Key not found !'
            }, 404
    except Exception as error:
        if DEBUG:
            print(error)
        return server_error.internal_server_error()
