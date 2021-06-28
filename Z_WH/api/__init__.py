from .router.auth import authRouter
from .router.token import tokenRouter
from .router.user import userRouter
from .router.timeSlots import timeSlotRouter
from .router.outGroup import outGroupRouter
from .router.temperature import temperatureRouter

from .app import app

from .responces import error


app.register_blueprint(authRouter)
app.register_blueprint(tokenRouter)
app.register_blueprint(userRouter)
app.register_blueprint(timeSlotRouter)
app.register_blueprint(outGroupRouter)
app.register_blueprint(temperatureRouter)
