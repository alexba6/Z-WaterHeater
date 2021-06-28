from Z_WH.api.middlewares import response, authentification
from Z_WH.services import userManager


@response.json
@authentification.checkUserKey
def regenerateKeyCtrl(**kwargs):
    logKey = userManager.regenerateKey(kwargs['keyId'])
    return {
        'keyId': logKey.id,
        'newKey': logKey.key
    }, 200


@response.json
@authentification.checkUserKey
def checkKeyCtrl(**kwargs):
    return {
        'message': 'VALID'
    }, 200
