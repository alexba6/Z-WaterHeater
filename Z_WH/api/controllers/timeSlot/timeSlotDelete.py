from Z_WH.api.middlewares import authentification, response
from Z_WH.services import autoTimeSlotManager


@response.json
@authentification.checkUserKey
def deleteTimeSlotCtrl(**kwargs):
    autoTimeSlotManager.deleteTimeSlot(kwargs['slotId'])

    return {
        'message': 'Time slot deleted !'
    }, 200
