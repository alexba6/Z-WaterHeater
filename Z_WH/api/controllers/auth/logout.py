from Z_WH.api.middlewares import response, authentification

from Z_WH.services import userManager


@response.json
@authentification.checkUserKey
def logoutCtrl(**kwargs):
    userManager.deleteKey(kwargs['keyId'])
    return {
        'message': 'Logout successfully !'
    }, 200
