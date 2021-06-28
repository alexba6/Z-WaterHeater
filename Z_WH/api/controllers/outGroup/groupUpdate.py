
from Z_WH.api.middlewares import authentification, response, schema
from Z_WH.services import groupManager
from Z_WH.services.output import GroupManagerError

from Z_WH.config.output import AVAILABLE_OUTPUTS

AVAILABLE_OUTPUTS_ID = [availableOutput[1] for availableOutput in AVAILABLE_OUTPUTS]


@response.json
@authentification.checkUserKey
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string'
        },
        'outId': {
            'type': 'array',
            'maxItems': len(AVAILABLE_OUTPUTS_ID)**2,
            'items': {
                'enum': AVAILABLE_OUTPUTS_ID,
            }
        }
    }
})
def updateGroupCtrl(**kwargs):
    json = kwargs['json']
    try:
        groupManager.updateGroup(kwargs['groupId'], json.get('outId'), json.get('name'))
    except GroupManagerError as error:
        return {
            'error': error.message
        }, 400
    return {
       'message': 'Group updated !'
    }, 200

