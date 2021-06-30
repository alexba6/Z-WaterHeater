
from Z_WH.api.middlewares import response, schema, authentification
from Z_WH.services import outputManager


@response.json
@authentification.checkUserKey
def getTempSaverSettings(**kwargs):
    return outputManager.getSettings(), 200


@response.json
@authentification.checkUserKey
@schema.schemaValidator(outputManager.getSettingsSchema())
def updateTempSaverSettings(**kwargs):
    outputManager.updateSettings(**kwargs.get('json'))
    return {
        'message': 'Output setting updated !'
    }, 200
