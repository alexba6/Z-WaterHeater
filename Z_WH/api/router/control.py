from flask import Blueprint
from Z_WH.api.controllers.control import controlGet

controlRouter = Blueprint('control', __name__, url_prefix='/api/control')

# Get output info
controlRouter.route(
    '',
    endpoint='getOutputInfo',
    methods=['GET']
)(controlGet.getControlOutputInfo)
