from flask import Blueprint
from Z_WH.api.controllers.temperature import tempGetDay

temperatureRouter = Blueprint('temperature', __name__, url_prefix='/api/temp')


# Get temperature
temperatureRouter.route(
    '',
    endpoint='getTemperature',
    methods=['GET']
)(tempGetDay.getTempDayCtrl)
