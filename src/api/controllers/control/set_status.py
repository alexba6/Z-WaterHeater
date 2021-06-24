from flask import request

from ....tools.log import logger
from ....models.User import WRITER
from ....services import operation_state
from ....utils.output import groupManager
from ...middlewares import auth, response
from ...responces import server_error


@response.format_json
@auth.check_user_key
@auth.check_role(WRITER)
def setStatus(**kwargs):
    try:
        state = kwargs.get('state').lower()
        if state == 'on':
            groupId = request.args.get('groupId')
            if groupId is None or not groupManager.groupExist(int(groupId)):
                return {
                    'error': 'The group does not exist !'
                }, 404
            operation_state.operation_sate.switchOn(int(groupId))
        elif state == 'off':
            operation_state.operation_sate.switchOff()
        elif state == 'auto':
            operation_state.operation_sate.switchAuto()
        else:
            return {
                'error': 'Unable to find the state',
                'availableStates': ['on', 'off', 'auto']
            }, 400
        return {
            'message': 'OK'
        }, 200
    except Exception as error:
        print(error)
        logger.error(error)
        return server_error.internal_server_error()
