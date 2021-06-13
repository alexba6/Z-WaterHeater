
from ...middlewares import auth, response, format_body
from ...responces import server_error

from ....models.User import ADMIN
from ....tools.log import logger
from ....services.temp_chart import temp_chart


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
def getTempChartSettingCtrl(**kwargs):
    try:
        config = temp_chart.getConfig()
        if config is None:
            return {
                'error': 'Temp chart configuration not found !'
            }, 400
        return config, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()


@response.format_json
@auth.check_user_key
@auth.check_role(ADMIN)
@format_body.body_json
@format_body.check_body(None, ['refreshInterval'])
def updateTempChartSettingCtrl(**kwargs):
    try:
        temp_chart.saveConfig(**kwargs['body'])
        return {
            'message': 'OK'
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()

