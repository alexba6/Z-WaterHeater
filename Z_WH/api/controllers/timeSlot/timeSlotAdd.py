from typing import List

from Z_WH.api.middlewares import authentification, response, schema
from Z_WH.tools.time import ISO_TIME_PATTERN
from Z_WH.services import autoTimeSlotManager
from Z_WH.services.autoTimeSlot import TimeSlot


@response.json
@authentification.checkUserKey
@schema.schemaValidator({
    'type': 'array',
    'minItems': 1,
    'items': [
        {
            'type': 'object',
            'properties': {
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
            'required': ['start', 'end', 'groupId']
        }
    ]
})
def addTimeSlotCtrl(**kwargs):
    json = kwargs['json']
    timeSlots: List[TimeSlot] = []

    for dataSlot in json:
        timeSlot = TimeSlot()
        timeSlot.startISO = dataSlot.get('start')
        timeSlot.endISO = dataSlot.get('end')
        timeSlot.groupId = dataSlot.get('groupId')
        timeSlots.append(timeSlot)

    autoTimeSlotManager.addUpdateTimeSlot(timeSlots)

    return {
        'message': 'Time slot added !',
        'timeSlotsAdded': [
            {
                'id': timeSlot.id,
                'start': timeSlot.startISO,
                'end': timeSlot.endISO,
                'groupId': timeSlot.groupId
            } for timeSlot in timeSlots
        ]
    }, 200
