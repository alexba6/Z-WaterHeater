from .router.auth import authRouter
from .router.control import controlRouter
from .router.group import groupRouter
from .router.setting import settingRouter
from .router.temp import tempRouter
from .router.token import tokenRouter
from .router.user import userRouter

from .app import app

from .responces import error


app.register_blueprint(authRouter)
app.register_blueprint(controlRouter)
app.register_blueprint(groupRouter)
app.register_blueprint(settingRouter)
app.register_blueprint(tempRouter)
app.register_blueprint(tokenRouter)
app.register_blueprint(userRouter)

