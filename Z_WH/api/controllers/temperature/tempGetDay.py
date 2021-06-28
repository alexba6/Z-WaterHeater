import datetime
from flask import request
from Z_WH.api.middlewares import response, authentification
from Z_WH.services import tempSaverManager


@response.json
@authentification.checkUserKey
def getTempDayCtrl(**kwargs):
    date = datetime.date.today()
    dateArg = request.args.get('date')
    if dateArg:
        try:
            date = datetime.date.fromisoformat(dateArg)
        except ValueError as error:
            return {
                'error': error.args
            }, 400

    tempData = tempSaverManager.read(date)
    if len(tempData) == 0:
        return {
           'error': 'No data found !'
        }, 404
    return {
        'date': date.isoformat(),
        'data': tempData
    }, 200
