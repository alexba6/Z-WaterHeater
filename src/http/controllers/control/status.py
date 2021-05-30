from ....tools.log import logger
from ....models.User import WRITER
from ....services import output
from ...middlewares import auth, response
from ...responces import server_error


@response.format_json
@auth.check_user_key
@auth.check_role(WRITER)
def status_ctrl(**kwargs):
    try:
        current_group = output.group_manager.get_group_by('id', kwargs['group_id'])
        if current_group:
            state = kwargs['state'].upper()
            if state in ['ON', 'OFF']:
                output.group_manager.switch_group(current_group, state == 'ON')
                return {
                    'message': 'Input ok !'
                }, 200
            else:
                return {
                    'error': 'State must be a ON or OFF !'
                }, 400
        else:
            return {
                'error': 'Group does not exist !'
            }, 404
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()
