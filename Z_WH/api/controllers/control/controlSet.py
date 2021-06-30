from flask import request

from Z_WH.api.middlewares import response, authentification
from Z_WH.services import outputManager


@response.json
@authentification.checkUserKey
def setControlState(**kwargs):
    mode = kwargs['mode']
    groupId = request.args.get('groupId')
    if mode == 'AUTO':
        outputManager.switchAUTO()
    elif mode == 'OFF':
        outputManager.switchOFF()
    elif mode == 'ON':
        outputManager.switchON(groupId)
    return {
        'message': 'Ok'
    }, 200
