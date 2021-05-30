from ....tools.log import logger
from ...responces import server_error
from ...middlewares import format_body, auth, response
from ....models.User import ADMIN
from ....services.output import group_manager


@response.format_json
@format_body.body_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.check_body(['name', 'outputs_name'])
def group_add_ctrl(**kwargs):
    try:
        body = kwargs['body']
        current_group = group_manager.get_group_by('name', body['name'])
        if not current_group:
            group_manager.group_add(body['name'], body['outputs_name'])
            return {
                'message': 'Groups added successfully !'
            }, 201
        else:
            return {
                'error': 'NAME_TAKEN'
            }, 400
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()
