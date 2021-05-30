from ....config.database import Session
from ....models import AuthorizationKey
from ....tools.log import logger
from ...middlewares import format_body, response
from ...responces import server_error


@response.format_json
@format_body.body_json
@format_body.check_body(['keyId', 'key'])
def logout_ctrl(**data):
    try:
        body = data.get('body')
        session = Session()
        authorization_key = session.query(AuthorizationKey) \
            .filter(AuthorizationKey.id == body['keyId']) \
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
                    'error': 'KEY_INVALID'
                }, 400
        else:
            return {
                'error': 'KEY_NOT_FOUND'
            }, 404
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


