
from Z_WH.api.middlewares import authentification, response
from Z_WH.models.User import READER
from Z_WH.services import tempSensorManager


@response.json
@authentification.checkUserKey(READER)
def getSensorsCtrl(**kwargs):
    return {
        'sensors': tempSensorManager.getSensorsInfo()
    }, 200



