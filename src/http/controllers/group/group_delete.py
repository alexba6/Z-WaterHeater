from ....tools.log import logger
from ...responces import server_error
from ...middlewares import auth, response
from ....models.User import ADMIN
from ....services.output import group_manager


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def group_delete_ctrl(**kwargs):
    try:
        group_id = kwargs['group_id']
        if not group_manager.get_group_by('id', group_id):
            return {
                'error': 'GROUP_NOT_FOUND'
            }, 404
        group_manager.group_del(group_id)
        return {
            'message': f"Group {group_id} deleted !"
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()

