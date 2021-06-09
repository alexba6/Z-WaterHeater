from flask import Blueprint
from ..controllers.control import status

controlRouter = Blueprint('control', __name__, url_prefix='/api/control')


controlRouter.route('/manuel-on/<group_id>', endpoint='manuel-on', methods=['POST'])(status.manuel_on)
controlRouter.route('/manuel-off', endpoint='manuel-off', methods=['POST'])(status.manuel_off)
