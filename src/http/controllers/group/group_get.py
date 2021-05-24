
from flask import jsonify

from ....config import DEBUG
from ...responces import server_error
from ...middlewares import auth
from ....models.User import ADMIN
from ....services.output import group_manager


@auth.check_user_key
@auth.check_role(ADMIN)
def group_get_all_ctrl(**kwargs):
    try:
        group_info = group_manager.groups_info()
        return jsonify({
            'groups': group_info
        }), 200
    except Exception as error:
        if DEBUG or 1:
            print(error)
        return server_error.internal_server_error()

