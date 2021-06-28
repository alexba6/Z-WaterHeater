
from Z_WH.services import groupManager
from Z_WH.api.middlewares import response, authentification


@response.json
@authentification.checkUserKey
def getGroupCtrl(**kwargs):
    return {
        'outGroups': [
            {
                'id': group.id,
                'outId': [output.id for output in group.outputs],
                'name': group.name
            } for group in groupManager.getGroups()
        ]
    }, 200
