from typing import List
from w1thermsensor import AsyncW1ThermSensor, Unit, Sensor
from ..tools.meta import MetaData
from ..tools.log import logger


class ThermSensor:
    def __init__(self, sensor_id: str, name: str = None):
        self._sensor = AsyncW1ThermSensor(Sensor.DS18B20, sensor_id)
        self.id = self._sensor.id
        self._name = name
        self._temp: float = None

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
            'name': self._name
        }

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        assert type(name) is not str, 'The sensor name must be a string value !'
        self._name = name


class TempManager:
    def __init__(self):
        self._meta = MetaData('temp-sensor')
        self._sensors: List[ThermSensor] = []

    # Init the temp sensors
    def init(self):
        if self._meta.data is None:
            try:
                for sensor in AsyncW1ThermSensor.get_available_sensors():
                    self._sensors.append(ThermSensor(sensor.id, f'Sensor @{sensor.id}'))
                self.saveMeta()
            except Exception as error:
                logger.error(error)
        else:
            for meta_sensor in self._meta.data:
                self._sensors.append(ThermSensor(
                    meta_sensor.get('id'),
                    meta_sensor.get('name')
                ))

    # Save the current temp sensor
    def saveMeta(self):
        self._meta.data = [sensor.getInfo() for sensor in self._sensors]

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
    def getSensorsId(self) -> List[str]:
        return [sensor.id for sensor in self._sensors]


temp_manager = TempManager()
