from typing import List

from Z_WH.api.middlewares import authentification, response, schema
from Z_WH.models.User import WRITER
from Z_WH.tools.time import ISO_TIME_PATTERN
from Z_WH.services import autoTimeSlotManager
from Z_WH.services.auto import TimeSlot, AutoTimeSlotManagerError


@response.json
@schema.schemaValidator({
    'type': 'array',
    'minItems': 1,
    'items': [
        {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'string'
                },
                'groupId': {
                    'type': 'string'
                },
                'start': {
                    'type': 'string',
                    'pattern': ISO_TIME_PATTERN
                },
                'end': {
                    'type': 'string',
                    'pattern':  ISO_TIME_PATTERN
                }
            },
            'required': ['id', 'start', 'end', 'groupId']
        }
    ]
})
@authentification.checkUserKey(WRITER)
def updateTimeSlotCtrl(**kwargs):
    json = kwargs['json']
    timeSlots: List[TimeSlot] = []

    for dataSlot in json:
        timeSlot = TimeSlot()
        timeSlot.id = dataSlot.get('id')
        timeSlot.startISO = dataSlot.get('start')
        try:
            timeSlot.endISO = dataSlot.get('end')
            timeSlot.groupId = dataSlot.get('groupId')
        except ValueError as error:
            return {
                'error': 'Invalid time format !'
            }, 400
        timeSlots.append(timeSlot)

    try:
        autoTimeSlotManager.addUpdateTimeSlot(timeSlots)
    except AutoTimeSlotManagerError as error:
        return {
            'error': error.message,
            'slotsId': [slot.id for slot in error.timeSlot]
        }, 400

    return {
        'message': 'Groups updated !'
    }, 200
