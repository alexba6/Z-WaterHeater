from flask import Blueprint
from Z_WH.api.controllers.tempSensors import tempSensorGet, tempSensorUpdate

tempSensorRouter = Blueprint('tempSensor', __name__, url_prefix='/api/sensor')


# Get temperature
tempSensorRouter.route(
    '',
    endpoint='getSensorInfo',
    methods=['GET']
)(tempSensorGet.getSensorsCtrl)

# Update sensor information
tempSensorRouter.route(
    '/<sensorId>',
    endpoint='updateSensor',
    methods=['POST']
)(tempSensorUpdate.updateTempSensorCtrl)
