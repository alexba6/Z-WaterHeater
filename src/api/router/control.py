from flask import Blueprint
from ..controllers.control import status

controlRouter = Blueprint('control', __name__, url_prefix='/api/control')


controlRouter.route('/switch/<state>', endpoint='switch', methods=['POST'])(status.switchCtrl)

