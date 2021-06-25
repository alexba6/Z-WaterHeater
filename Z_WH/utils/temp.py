import threading
from typing import List
from w1thermsensor import AsyncW1ThermSensor, Unit, Sensor

from Z_WH.tools.meta import MetaData


class ThermSensor:
    def __init__(self, sensorId: str, name: str, alive: bool, color: str = None):
        self.id = sensorId
        self.alive: bool = alive
        self.color: str or None = color
        self.name = name

        self._sensor = AsyncW1ThermSensor(Sensor.DS18B20, sensorId)
        self._temp: float = 0

    # Refresh and get the temperature from the sensor
    async def getTemp(self) -> float:
        self._temp = await self._sensor.get_temperature(Unit.DEGREES_C)
        return self._temp

    # Get the old temperature save in cache
    def getTempCache(self):
        return self._temp

    # Get the information about the sensor
    def getInfo(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }


class TempManager:
    def __init__(self):
        self._sensors: List[ThermSensor] = []

        self._refreshAliveSensorsTimer = None

        self._metaSensors = MetaData('temp-sensor')

    # Init the temp sensors
    def init(self):
        self.loadMeta()
        self._refreshAliveSensors()

    # Load the sensors from meta
    def loadMeta(self):
        metaSensors = self._metaSensors.data
        if metaSensors:
            for metaSensor in metaSensors:
                self._sensors.append(ThermSensor(
                    metaSensor.get('sensorId'),
                    metaSensor.get('name'),
                    metaSensor.get('alive'),
                    metaSensor.get('color')
                ))

    # Refresh alive temp sensors
    def _refreshAliveSensors(self):
        self._refreshAliveSensorsTimer = threading.Timer(10, lambda: self._refreshAliveSensors())
        self._refreshAliveSensorsTimer.start()

        aliveSensors = AsyncW1ThermSensor.get_available_sensors()
        aliveSensorsId = [sensor.id for sensor in aliveSensors]
        currentSensorsId = [sensor.id for sensor in self._sensors]

        saveMeta = False
        for currentSensor in self._sensors:
            isAlive = currentSensor.id in aliveSensorsId
            if currentSensor.alive != isAlive:
                currentSensor.alive = isAlive
                saveMeta = True

        for aliveSensorId in aliveSensorsId:
            if aliveSensorId not in currentSensorsId:
                self._sensors.append(ThermSensor(
                    aliveSensorId,
                    f"Sensor @{aliveSensorId}",
                    True
                ))
                saveMeta = True

        if saveMeta:
            self.saveMeta()

    # Save the meta data
    def saveMeta(self):
        self._metaSensors.data = [
            {
                'sensorId': sensor.id,
                'name': sensor.name,
                'alive': sensor.alive,
                'color': sensor.color
            }
            for sensor in self._sensors
        ]

    # Find a sensor with his id
    def getSensorById(self, sensor_id) -> ThermSensor:
        for sensor in self._sensors:
            if sensor.id == sensor_id:
                return sensor
        raise Exception('Cannot find the sensor !')

    # Rename a sensor with his id
    def sensorRename(self, sensor_id: str, name: str):
        self.getSensorById(sensor_id).name = name
        self.saveMeta()

    # Change color sensor with his id
    def sensorChangeColor(self, sensor_id: str, color: str):
        self.getSensorById(sensor_id).name = color
        self.saveMeta()

    # Get the temperature from the sensor by id
    async def getTemp(self, sensorId: str) -> float:
        return await self.getSensorById(sensorId).getTemp()

    # Get sensor name
    def getName(self, sensorId: str) -> str:
        return self.getSensorById(sensorId).name

    # Get the temperature from the sensor cache by id
    def getTempCache(self, sensorId: str) -> float:
        return self.getSensorById(sensorId).getTempCache()

    # Get all sensor id
    @classmethod
    def getSensorsId(cls) -> List[int]:
        return [sensor.id for sensor in AsyncW1ThermSensor.get_available_sensors()]


temp_manager = TempManager()