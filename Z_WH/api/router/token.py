from flask import Blueprint
from Z_WH.api.controllers.token import code

tokenRouter = Blueprint('token', __name__, url_prefix='/api/token')


# Generate code route
tokenRouter.route(
    '/generate-code',
    endpoint='generateCode',
    methods=['GET']
)(code.generateCodeCtrl)

# Check code route
tokenRouter.route(
    '/check-code',
    endpoint='checkCode',
    methods=['POST']
)(code.checkCodeCtrl)
