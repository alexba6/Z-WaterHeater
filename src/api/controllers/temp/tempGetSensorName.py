from ...middlewares import auth, response
from ...responces import server_error
from ....tools.log import logger
from ....utils.temp import temp_manager


@response.format_json
@auth.check_user_key
def tempGeSensorNameCtrl(**kwargs):
    try:
        return {
            'sensors': [
                {
                    'id': sensorId,
                    'name': temp_manager.getName(sensorId)
                }
                for sensorId in temp_manager.getSensorsId()
            ]
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()
