import csv
import threading
import schedule
from os import makedirs, path
import datetime

from Z_WH.tools.meta import MetaData
from .tempSensor import TempSensorManager

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
                        'value': float(t.split('@')[0]),
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


class TempSaverManager:
    def __init__(self, tempSensorManager: TempSensorManager):
        self._tempSensorManager = tempSensorManager
        self._dayTempCache = []
        self._dayTempPath = None
        self._refreshTempIntervalTime = 120
        self._saveTempTimer = None

        self._meta = MetaData('temp-chart')

    # Load the configuration and start temp service
    def init(self):
        self.loadMeta()
        self.loadDayPath()

        # Init the day cache at start
        self._dayTempCache = _readTempFile(datetime.date.today())

        schedule.every(1).day.at('00:00:00').do(lambda: self.loadDayPath())
        self.saveTemps()

    # Load the day temp path
    def loadDayPath(self):
        now = datetime.date.today()
        dayTemp = _getDir(now)

        self._dayTempPath = _getPath(now)

        if not path.exists(dayTemp):
            makedirs(dayTemp)

        # Clear the day cache
        self._dayTempCache.clear()

    # Load the temp meta data
    def loadMeta(self):
        if self._meta.data is None:
            self._meta.data = {
                'refreshInterval': self._refreshTempIntervalTime
            }
        else:
            self._refreshTempIntervalTime = self._meta.data.get('refreshInterval')

    # Get the temp chart configuration
    def getConfig(self):
        return {
            'refreshInterval': self._refreshTempIntervalTime
        }

    # set the temp chart configuration
    def saveConfig(self, **kwargs):
        if kwargs.get('refreshInterval'):
            self._refreshTempIntervalTime = kwargs['refreshInterval']
        self.saveMeta()

    # Save the temp chart meta
    def saveMeta(self):
        self._meta.data = {
            'refreshInterval': self._refreshTempIntervalTime
        }

    # Save the temperature in CSV each x seconds
    def saveTemps(self):
        self._saveTempTimer = threading.Timer(
            self._refreshTempIntervalTime,
            lambda: self.saveTemps()
        )
        self._saveTempTimer.start()

        sensorsId = self._tempSensorManager.getAliveSensorsId()
        if len(sensorsId) == 0:
            return

        time = datetime.datetime.now().strftime('%H-%M-%S')
        temp = {
            'time': time,
            'temp': [
                {
                    'value': self._tempSensorManager.getTemp(sensorId),
                    'sensorId': sensorId
                }
                for sensorId in sensorsId
            ]
        }
        self._dayTempCache.append(temp)
        _writeTempFile(datetime.date.today(), temp)

    # Read the temperature of one day from the cache if it is possible
    def read(self, date: datetime.date = datetime.date.today()):
        if date == datetime.date.today():
            return self._dayTempCache
        return _readTempFile(date)
