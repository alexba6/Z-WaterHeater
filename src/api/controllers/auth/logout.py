from ....config.database import Session
from ....tools.log import logger
from ...middlewares import response, auth
from ...responces import server_error


@response.format_json
@auth.check_user_key
def logout_ctrl(**kwargs):
    try:
        with Session() as session:
            session.delete(session.merge(kwargs['key']))
            session.commit()
            return {
                'message': 'Logout successfully !'
            }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


