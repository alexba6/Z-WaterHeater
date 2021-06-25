from .router.auth import authRouter
from .router.token import tokenRouter
from .router.user import userRouter

from .app import app

from .responces import error


app.register_blueprint(authRouter)
app.register_blueprint(tokenRouter)
app.register_blueprint(userRouter)

