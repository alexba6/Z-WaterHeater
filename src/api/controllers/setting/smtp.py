
from ...middlewares import auth, response, format_body
from ...responces import server_error

from ....models.User import ADMIN
from ....tools.log import logger
from ....services.mail import mail


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.body_json
@format_body.check_body(None, ['host', 'port', 'login', 'password'])
def updateSMTPSettingCtrl(**kwargs):
    try:
        mail.saveConfig(**kwargs['body'])
        return {
            'message': 'OK'
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def getSMTPSettingCtrl(**kwargs):
    try:
        config = mail.getConfig()
        if config is None:
            return {
                'error': 'SMTP configuration not found !'
            }, 400
        return config, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()

