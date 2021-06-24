from typing import List
from w1thermsensor import AsyncW1ThermSensor, Unit, Sensor

from ..config.database import Session
from ..models.TempSensor import TempSensor


class ThermSensor:
    def __init__(self, sensorId: str, name: str):
        self._sensor = AsyncW1ThermSensor(Sensor.DS18B20, sensorId)
        self.id = sensorId
        self.name = name
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
            'name': self.name
        }


class TempManager:
    def __init__(self):
        self._sensors: List[ThermSensor] = []

    # Init the temp sensors
    def init(self):
        with Session() as session:
            for sensor in session.query(TempSensor).all():
                self._sensors.append(ThermSensor(
                    sensor.sensor_id,
                    sensor.name
                ))

        availableSensors = AsyncW1ThermSensor.get_available_sensors()
        if len(self._sensors) == 0 and len(availableSensors) != 0:
            with Session() as session:
                for sensor in availableSensors:
                    tSensor = TempSensor()
                    tSensor.sensor_id = sensor.id
                    tSensor.name = f'Sensor @{sensor.id}'
                    session.add(tSensor)
                session.commit()
            self.init()

    # Find a sensor with his id
    def getSensorById(self, sensor_id) -> ThermSensor:
        for sensor in self._sensors:
            if sensor.id == sensor_id:
                return sensor
        raise Exception('Cannot find the sensor !')

    # Rename a sensor with his id
    def sensorRename(self, sensor_id: str, name: str):
        self.getSensorById(sensor_id).name = name

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
