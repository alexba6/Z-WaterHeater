
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
    },
    'required': ['name', 'outId']
})
def addGroupCtrl(**kwargs):
    json = kwargs['json']
    try:
        group = groupManager.addGroup(json['outId'], json['name'])

    except GroupManagerError as error:
        return {
            'error': error.message
        }, 400
    return {
       'message': 'Group added !',
       'group': {
           'id': group.id,
           'name': group.name,
           'outId': [output.id for output in group.outputs]
       }
    }, 200

