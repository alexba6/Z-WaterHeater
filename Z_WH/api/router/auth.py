from flask import Blueprint
from Z_WH.api.controllers.auth import login, logout, key

authRouter = Blueprint('auth', __name__, url_prefix='/api/auth')


# Login user route
authRouter.route(
    '/login',
    endpoint='login',
    methods=['POST']
)(login.loginCtrl)

# Renew user key route
authRouter.route(
    '/key-renew',
    endpoint='keyRenew',
    methods=['POST']
)(key.regenerateKeyCtrl)

# Check user key route
authRouter.route(
    '/key-check',
    endpoint='keyCheck',
    methods=['POST']
)(key.checkKeyCtrl)

# Logout user route
authRouter.route(
    '/logout',
    endpoint='logout',
    methods=['POST']
)(logout.logoutCtrl)
