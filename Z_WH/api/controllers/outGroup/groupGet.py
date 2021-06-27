
from Z_WH.services import groupManager


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

