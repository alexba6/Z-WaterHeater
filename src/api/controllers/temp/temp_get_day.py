from flask import request
import datetime

from ...middlewares import auth, response
from ....services import temp_chart
from ...responces import server_error
from ....tools.log import logger


@response.format_json
@auth.check_user_key
def tempGetDayCtrl(**kwargs):
    try:
        date = datetime.date.today()
        if request.args.get('day'):
            date = datetime.date.fromisoformat(request.args.get('day'))
        print(date)
        temp_data = temp_chart.temp_chart.read(date)
        if len(temp_data) == 0:
            return {
                'error': 'No data found !'
            }, 404
        return {
            'date': date.isoformat(),
            'data': temp_data
        }, 200
    except Exception as error:
        logger.error(error)
        return server_error.internal_server_error()