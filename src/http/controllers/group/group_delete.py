
from flask import jsonify

from ....config import DEBUG
from ...responces import server_error
from ...middlewares import auth, format_body
from ....models.User import ADMIN
from ....services.output import group_manager


@auth.check_user_key
@auth.check_role(ADMIN)
def group_delete_ctrl(**kwargs):
    try:
        name = kwargs['name']
        if not group_manager.get_group_from_name(name):
            return jsonify({
                'error': 'GROUP_NOT_FOUND'
            }), 404
        group_manager.group_del(name)
        return jsonify({
            'message': f"Group {name} deleted !"
        }), 200
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()

