
from ....tools.log import logger
from ...responces import server_error
from ...middlewares import auth, response
from ....models.User import ADMIN
from ....services.output import group_manager


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def group_get_all_ctrl(**kwargs):
    try:
        group_info = group_manager.groups_info()
        return {
            'groups': group_info
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()
