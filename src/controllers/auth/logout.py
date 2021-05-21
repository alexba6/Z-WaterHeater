from ...config import DEBUG
from ...config.database import Session
from ...models import AuthorizationKey
from ...responces import server_error
from ...middlewares import format_body


@format_body.body_json
@format_body.check_body(['key_id', 'key'])
def logout_ctrl(**data):
    try:
        body = data.get('body')
        session = Session()
        authorization_key = session.query(AuthorizationKey) \
            .filter(AuthorizationKey.id == body['key_id']) \
            .first()
        if isinstance(authorization_key, AuthorizationKey):
            if authorization_key.key == body['key']:
                session.delete(authorization_key)
                session.commit()
                return {
                    'message': 'Logout successfully !'
                }, 200
            else:
                return {
                    'error': 'Invalid key !'
                }, 400
        else:
            return {
                'error': 'Key not found !'
            }, 404
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()


