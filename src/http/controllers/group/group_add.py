
from flask import jsonify

from ....config import DEBUG
from ...responces import server_error
from ...middlewares import format_body, auth
from ....models.User import ADMIN
from ....services.output import group_manager


@format_body.body_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.check_body(['name', 'outputs_name'])
def group_add_ctrl(**kwargs):
    try:
        body = kwargs['body']
        if not group_manager.exist_groups(body['name']):
            group_manager.group_add(body['name'], body['outputs_name'])
            return jsonify({
                'message': 'Groups added successfully !'
            }), 201
        else:
            return jsonify({
                'error': 'NAME_TAKEN'
            }), 400
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()

