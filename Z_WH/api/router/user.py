from flask import Blueprint
from Z_WH.api.controllers.users import userAdd, userUpdate, userGet

userRouter = Blueprint('user', __name__, url_prefix='/api/user')

# Init the user route
userRouter.route(
    '',
    endpoint='initUser',
    methods=['POST']
)(userAdd.initUser)


# Update user route
userRouter.route(
    '',
    endpoint='updateUser',
    methods=['PUT']
)(userUpdate.updateUser)

# Update user route
userRouter.route(
    '',
    endpoint='getUser',
    methods=['GET']
)(userGet.getUser)
