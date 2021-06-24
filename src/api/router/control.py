from flask import Blueprint
from ..controllers.control import set_status, get_status

controlRouter = Blueprint('control', __name__, url_prefix='/api/control')


controlRouter.route('', endpoint='getStatus', methods=['GET'])(get_status.getStatusCtrl)
controlRouter.route('/<state>', endpoint='setStatus', methods=['POST'])(set_status.setStatus)
