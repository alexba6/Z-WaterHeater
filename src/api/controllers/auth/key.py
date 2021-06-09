import datetime

from ....models import AuthorizationKey
from ....config.database import Session
from ....tools.log import logger
from ...middlewares import format_body, response
from ...responces import server_error


@response.format_json
@format_body.body_json
@format_body.check_body(['keyId', 'key'])
def regenerate_key_ctrl(**data):
    try:
        body = data.get('body')
        date = datetime.datetime.now()
        with Session() as session:
            authorization_key = session.query(AuthorizationKey)\
                .filter(AuthorizationKey.id == body['keyId'])\
                .first()
            if authorization_key:
                if authorization_key.match_key(body['key']):
                    authorization_key.last_generated = date
                    key = authorization_key.generate_key()
                    session.commit()
                    return {
                        'keyId': authorization_key.id,
                        'newKey': key
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
