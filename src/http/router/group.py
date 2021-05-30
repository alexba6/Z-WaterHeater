from flask import Blueprint
from ..controllers.group import group_add, group_get, group_delete, group_update

groupRouter = Blueprint('out-group', __name__, url_prefix='/api/out-group')


groupRouter.route('/', endpoint='group_get_all', methods=['GET'])(group_get.group_get_all_ctrl)
groupRouter.route('/', endpoint='group_add', methods=['POST'])(group_add.group_add_ctrl)
groupRouter.route('/<group_id>', endpoint='group_delete', methods=['DELETE'])(group_delete.group_delete_ctrl)
groupRouter.route('/<group_id>', endpoint='group_update', methods=['PUT'])(group_update.group_update_ctrl)
