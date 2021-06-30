
from Z_WH.api.middlewares import response, schema, authentification
from Z_WH.services import tempSaverManager


@response.json
@authentification.checkUserKey
def getTempSaverSettings(**kwargs):
    return tempSaverManager.getSettings(), 200


@response.json
@authentification.checkUserKey
@schema.schemaValidator(tempSaverManager.getSettingsSchema())
def updateTempSaverSettings(**kwargs):
    json = kwargs.get('json')
    tempSaverManager.updateSettings(**json)
    return {
        'message': 'Temp saver setting updated !'
    }, 200
