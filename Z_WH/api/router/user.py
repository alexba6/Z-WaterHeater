from flask import Blueprint
from Z_WH.api.controllers.users import userAdd, userReset, userDelete

userRouter = Blueprint('user', __name__, url_prefix='/api/user')

# Add user route
userRouter.route(
    '',
    endpoint='addUser',
    methods=['POST']
)(userAdd.addUserCtrl)

# Add admin user route
userRouter.route(
    '/admin',
    endpoint='addAdmin',
    methods=['POST']
)(userAdd.addAdminCtrl)

# Reset user password route
userRouter.route(
    '/reset-password/<userId>',
    endpoint='resetUserPassword',
    methods=['POST']
)(userReset.resetUserPasswordCtrl)

# Delete user route
userRouter.route(
    '/<userId>',
    endpoint='deleteUser',
    methods=['DELETE']
)(userDelete.delUserCtrl)
