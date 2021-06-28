from Z_WH.api.middlewares import authentification, response

from Z_WH.services import userManager


@response.json
@authentification.checkUserKey
def getUser(**kwargs):
    return {
        'email': userManager.email
    }, 200
