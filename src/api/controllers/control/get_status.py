from ...responces import server_error
from ...middlewares import response, auth
from ....models.User import READER
from ....tools.log import logger
from ....services import operation_state


@response.format_json
@auth.check_user_key
@auth.check_role(READER)
def getStatusCtrl(**kwargs):
    try:
        return operation_state.operation_sate.getMode(), 200
    except Exception as error:
        print(error)
        logger.error(error)
        return server_error.internal_server_error()
