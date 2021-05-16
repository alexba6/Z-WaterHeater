from flask import Blueprint
from ..controllers.users import user_add

userRouter = Blueprint('user', __name__, url_prefix='/api/user')

userRouter.route('/', endpoint='add_user', methods=['POST'])(user_add.add_user_ctrl)

