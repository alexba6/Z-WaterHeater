
from Z_WH.api.middlewares import authentification, response
from Z_WH.services import tempSensorManager


@response.json
@authentification.checkUserKey
def getSensorsCtrl(**kwargs):
    return {
        'sensors': tempSensorManager.getSensorsInfo()
    }, 200



