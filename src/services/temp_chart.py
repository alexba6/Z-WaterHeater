import asyncio
import csv
import threading
from os import makedirs, path
import datetime
from ..utils.temp import temp_manager
from ..tools.meta import MetaData


DATA_DIR = './data/temp'


# Get the CSV  folder dir
def _getDir(date: datetime.date = datetime.date.today()):
    return path.join(
        DATA_DIR,
        str(date.year),
        str(date.month)
    )


# Get the CSV file path
def _getPath(date:  datetime.date):
    return path.join(
        _getDir(date),
        f"temp-{str(date.strftime('%m-%d-%Y'))}.csv"
    )


# Read the temp data of CSV file
def _readTempFile(date: datetime.date):
    data = []
    with open(_getPath(date), 'r', encoding='utf-8') as file:
        for time, *temp in csv.reader(file):
            data.append({
                'time': time,
                'temp': [
                    {
                        'value': t.split('@')[0],
                        'sensorId': t.split('@')[1],
                    }
                    for t in temp
                ]
            })
    return data


# Write the temp data in CSV file
def _writeTempFile(date: datetime.date, temp):
    with open(_getPath(date), 'a', encoding='utf-8') as file:
        data = [f"{temp['value']}@{temp['sensorId']}" for temp in temp['temp']]
        file.write(f"{temp['time']}, {', '.join(data)}\n")


class TempChart:
    def __init__(self):
        self._dayTemp = []
        self._dayPath = None
        self._meta = MetaData('temp-chart')

    # Load the configuration and start temp service
    def load(self):
        date = datetime.date.today()

        self._dayPath = _getPath(date)

        if not path.exists(_getDir(date)):
            makedirs(_getDir(date))

        if self._meta.data is None:
            self._meta.data = {
                'refreshDelta': 20
            }

        for d in _readTempFile(date):
            print(d)

        asyncio.run(self.saveTemps())

    # Save the temperature in CSV each x seconds
    async def saveTemps(self):
        def startTimer():
            asyncio.run(self.saveTemps())
        refresh_delta = self._meta.data.get('refreshDelta')
        threading.Timer(refresh_delta if refresh_delta is int or float else 30, startTimer).start()
        time = datetime.datetime.now().strftime('%H-%M-%S')
        temp = {
            'time': time,
            'temp': [
                {
                    'value': await temp_manager.getTemp(sensor_id),
                    'sensorId': sensor_id
                }
                for sensor_id in temp_manager.getSensorsId()
            ]
        }
        self._dayTemp.append(temp)
        _writeTempFile(datetime.date.today(), temp)


temp_chart = TempChart()
