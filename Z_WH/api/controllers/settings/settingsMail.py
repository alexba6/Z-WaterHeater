
from Z_WH.api.middlewares import response, schema, authentification
from Z_WH.services import mailManager


@response.json
@authentification.checkUserKey
def getMailSettings(**kwargs):
    return mailManager.getSettings(), 200


@response.json
@authentification.checkUserKey
@schema.schemaValidator(mailManager.getSettingsSchema())
def updateMailSettings(**kwargs):
    mailManager.updateSettings(**kwargs.get('json'))
    return {
        'message': 'Mail settings updated !'
    }, 200
