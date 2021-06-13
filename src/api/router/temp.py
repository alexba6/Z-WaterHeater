from flask import Blueprint
from ..controllers.temp import temp_get_day, tempGetSensorName

tempRouter = Blueprint('temperature', __name__, url_prefix='/api/temp')

tempRouter.route('', endpoint='temp-get-day', methods=['GET'])(temp_get_day.tempGetDayCtrl)
tempRouter.route('/sensor-name', endpoint='get-sensor-name', methods=['GET'])(tempGetSensorName.tempGeSensorNameCtrl)
