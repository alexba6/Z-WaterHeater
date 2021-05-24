
from flask import jsonify

from ....config import DEBUG
from ...responces import server_error
from ...middlewares import auth, format_body
from ....models.User import ADMIN
from ....services.output import group_manager


@format_body.body_json
@format_body.check_body(None, ['name', 'outputs_name'])
@auth.check_user_key
@auth.check_role(ADMIN)
def group_update_ctrl(**kwargs):
    try:
        body = kwargs['body']
        if not group_manager.get_group_from_name(kwargs['name']):
            return jsonify({
                'error': 'GROUP_NOT_FOUND'
            }), 404

        name = body.get('name')
        outputs_name = body.get('outputs_name')

        if name:
            if name == kwargs['name']:
                return jsonify({
                    'error': 'GROUP_NAME_UNCHANGED'
                }), 400
            if group_manager.get_group_from_name(body['name']):
                return jsonify({
                    'error': 'NAME_TAKEN'
                }), 400

        group_manager.group_update(kwargs['name'], new_name=name, outputs_name=outputs_name)
        return jsonify({
            'message': 'Group updated !'
        }), 200

    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()

