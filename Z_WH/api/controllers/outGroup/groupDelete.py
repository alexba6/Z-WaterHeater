
from Z_WH.api.middlewares import authentification, response
from Z_WH.services import groupManager
from Z_WH.services.output import GroupManagerError


@response.json
@authentification.checkUserKey
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

