from ....tools.log import logger
from ....models.User import WRITER
from ....utils import output
from ...middlewares import auth, response
from ...responces import server_error


@response.format_json
@auth.check_user_key
@auth.check_role(WRITER)
def manuel_on(**kwargs):
    try:
        output.group_manager.switchOn(int(kwargs['group_id']))
        return {
            'message': 'Input ok !'
        }, 200
    except Exception as error:
        print(error)
        logger.error(error)
        return server_error.internal_server_error()


@response.format_json
@auth.check_user_key
@auth.check_role(WRITER)
def manuel_off(**kwargs):
    try:
        output.group_manager.switchOff()
        return {
                   'message': 'Input ok !'
               }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()
