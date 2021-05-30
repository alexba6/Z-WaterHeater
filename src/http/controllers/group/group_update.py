
from ....tools.log import logger
from ...responces import server_error
from ...middlewares import auth, format_body, response
from ....models.User import ADMIN
from ....services.output import group_manager


@response.format_json
@format_body.body_json
@format_body.check_body(None, ['name', 'outputs_name'])
@auth.check_user_key
@auth.check_role(ADMIN)
def group_update_ctrl(**kwargs):
    try:
        body = kwargs['body']
        current_group = group_manager.get_group_by('id', kwargs['group_id'])
        if not current_group:
            return {
                'error': 'GROUP_NOT_FOUND'
            }, 404

        name = body.get('name')
        outputs_name = body.get('outputs_name')

        if name:
            if name == current_group.name:
                return {
                    'error': 'GROUP_NAME_UNCHANGED'
                }, 400
            if group_manager.get_group_by('name', name):
                return {
                    'error': 'NAME_TAKEN'
                }, 400

        group_manager.group_update(current_group, new_name=name, outputs_name=outputs_name)
        return {
            'message': 'Group updated !'
        }, 200

    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()

