
from Z_WH.api.middlewares import authentification, response, schema
from Z_WH.services import tempSensorManager
from Z_WH.services.tempSensor import TempSensorManagerError


@response.json
@authentification.checkUserKey
@schema.schemaValidator({
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
            'minLength': 2,
            'maxLength': 6
        },
        'color': {
            'type': 'string',
            'pattern': '^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$'
        },
        'displayOnScreen': {
            'type': 'boolean'
        }
    }
})
def updateTempSensorCtrl(**kwargs):
    json = kwargs['json']
    try:
        tempSensorManager.sensorUpdate(
            kwargs['sensorId'],
            name=json.get('name'),
            color=json.get('color'),
            displayOnScreen=json.get('displayOnScreen')
        )
    except TempSensorManagerError as e:
        return {
            'error': e.error
        }, 400
    return {
        'message': 'Sensor updated !'
    }, 200
