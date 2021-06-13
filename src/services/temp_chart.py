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
def _getPath(date: datetime.date):
    return path.join(
        _getDir(date),
        f"temp-{str(date.strftime('%m-%d-%Y'))}.csv"
    )


# Read the temp data of CSV file
def _readTempFile(date: datetime.date):
    temp_path = _getPath(date)
    if not path.exists(temp_path):
        return []
    data = []
    with open(temp_path, 'r', encoding='utf-8') as file:
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
        self._refreshInterval = 120
        self._meta = MetaData('temp-chart')
        self._timer_temp = None

    # Load the configuration and start temp service
    def load(self):
        date = datetime.date.today()
        self._dayPath = _getPath(date)
        dayDir = _getDir(date)
        if not path.exists(dayDir):
            makedirs(dayDir)
        self._dayTemp = _readTempFile(date)
        if self._meta.data is None:
            self._meta.data = {
                'refreshInterval': self._refreshInterval
            }
        else:
            self._refreshInterval = self._meta.data.get('refreshInterval')
        if self._timer_temp:
            self._timer_temp.cancel()
        asyncio.run(self.saveTemps())

    # Get the temp chart configuration
    def getConfig(self):
        if self._meta.data is None:
            return None
        return {
            'refreshInterval': self._refreshInterval
        }

    # set the temp chart configuration
    def saveConfig(self, **kwargs):
        if kwargs.get('refreshInterval'):
            self._refreshInterval = kwargs['refreshInterval']
        self.saveMeta()
        self.load()

    # Save the temp chart meta
    def saveMeta(self):
        self._meta.data = {
            'refreshInterval': self._refreshInterval
        }

    # Save the temperature in CSV each x seconds
    async def saveTemps(self):
        self._timer_temp = threading.Timer(
            self._refreshInterval,
            lambda: asyncio.run(self.saveTemps())
        )
        self._timer_temp.start()

        print(f'{datetime.datetime.now().isoformat()} > SAVE TEMP {self._refreshInterval}')

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

    # Read the temperature of one day from the cache if it is possible
    def read(self, date: datetime.date = datetime.date.today()):
        if date == datetime.date.today():
            return self._dayTemp
        return _readTempFile(date)


temp_chart = TempChart()
