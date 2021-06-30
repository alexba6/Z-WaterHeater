
from Z_WH.api.middlewares import response, authentification
from Z_WH.services import outputManager


@response.json
@authentification.checkUserKey
def getControlOutputInfo(**kwargs):
    return outputManager.getInfoControl(), 200

