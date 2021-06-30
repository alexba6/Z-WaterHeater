
from Z_WH.api.middlewares import response, authentification, schema
from Z_WH.services import tempLimitManager
from Z_WH.services.tempSensor import TempSensorManagerError


@response.json
@authentification.checkUserKey
def getTempLimitSettings(**kwargs):
    return tempLimitManager.getSettings(), 200


@response.json
@authentification.checkUserKey
@schema.schemaValidator(tempLimitManager.getSettingsSchema())
def updateTempLimitSettings(**kwargs):
    try:
        tempLimitManager.updateSettings(**kwargs.get('json'))
    except TempSensorManagerError as error:
        return {
            'message': error.error
        }, 400
    return {
        'message': 'Temp limit settings updated !'
    }, 200
