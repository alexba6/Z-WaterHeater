from .router.auth import authRouter
from .router.token import tokenRouter
from .router.user import userRouter
from .router.timeSlots import timeSlotRouter
from .router.outGroup import outGroupRouter
from .router.temperature import temperatureRouter
from .router.tempSensor import tempSensorRouter
from .router.settings import settingsRouter
from .router.control import controlRouter

from .app import app

from .responces import error


app.register_blueprint(authRouter)
app.register_blueprint(tokenRouter)
app.register_blueprint(userRouter)
app.register_blueprint(timeSlotRouter)
app.register_blueprint(outGroupRouter)
app.register_blueprint(temperatureRouter)
app.register_blueprint(tempSensorRouter)
app.register_blueprint(settingsRouter)
app.register_blueprint(controlRouter)
