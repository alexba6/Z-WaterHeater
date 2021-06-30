from flask import Blueprint
from Z_WH.api.controllers.control import controlGet, controlSet

controlRouter = Blueprint('control', __name__, url_prefix='/api/control')

# Get output info
controlRouter.route(
    '',
    endpoint='getOutputInfo',
    methods=['GET']
)(controlGet.getControlOutputInfo)

# Set control state
controlRouter.route(
    '/<mode>',
    endpoint='setControlState',
    methods=['POST']
)(controlSet.setControlState)
