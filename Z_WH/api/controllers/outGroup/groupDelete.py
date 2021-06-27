
from Z_WH.api.middlewares import authentification, response
from Z_WH.services import groupManager
from Z_WH.services.output import GroupManagerError
from Z_WH.models.User import WRITER


@response.json
@authentification.checkUserKey(WRITER)
def deleteGroupCtrl(**kwargs):
    try:
        groupManager.deleteGroup(kwargs['groupId'])
    except GroupManagerError as error:
        return {
            'error': error.message
        }, 400
    return {
       'message': 'Group deleted !'
    }, 200

