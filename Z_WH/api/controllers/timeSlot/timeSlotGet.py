from Z_WH.api.middlewares import authentification, response
from Z_WH.services import autoTimeSlotManager


@response.json
@authentification.checkUserKey
def getTimeSlotCtrl(**kwargs):
    return {
        'timeSlots': [{
            'id': timeSlot.id,
            'groupIp': timeSlot.id,
            'start': timeSlot.startISO,
            'end': timeSlot.endISO
        } for timeSlot in autoTimeSlotManager.getTimeSlot()]
    }, 200
