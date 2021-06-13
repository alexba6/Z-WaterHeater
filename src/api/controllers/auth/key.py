import datetime

from ....models import AuthorizationKey
from ....config.database import Session
from ....tools.log import logger
from ...middlewares import response, auth
from ...responces import server_error


@response.format_json
@auth.check_user_key
def regenerate_key_ctrl(**kwargs):
    try:
        with Session() as session:
            authorization_key: AuthorizationKey = kwargs['key']
            date = datetime.datetime.now()

            authorization_key.last_generated = date
            key = authorization_key.generate_key()
            session.add(session.merge(authorization_key))
            session.commit()

            return {
                'keyId': authorization_key.id,
                'newKey': key
            }, 200
    except Exception as error:
        print(error)
        logger.error(error)
        return server_error.internal_server_error()


@response.format_json
@auth.check_user_key
def checkKeyCtrl(**kwargs):
    return {
        'message': 'VALID'
    }, 200
