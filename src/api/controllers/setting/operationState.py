
from ...middlewares import auth, response, format_body
from ...responces import server_error

from ....models.User import ADMIN
from ....tools.log import logger
from ....services.operation_state import operation_sate


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.body_json
@format_body.check_body(None, ['autoCallbackTime'])
def updateOperationStateSettingCtrl(**kwargs):
    try:
        operation_sate.saveConfig(**kwargs['body'])
        return {
            'message': 'OK'
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def getOperationStateSettingCtrl(**kwargs):
    try:
        config = operation_sate.getConfig()
        if config is None:
            return {
                'error': 'Operation state configuration not found !'
            }, 400
        return config, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()

