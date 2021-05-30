from flask import Blueprint
from ..controllers.control import status

controlRouter = Blueprint('control', __name__, url_prefix='/api/control')


controlRouter.route('/status/<group_id>/<state>', endpoint='status', methods=['POST'])(status.status_ctrl)
