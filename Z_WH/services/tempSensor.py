import threading
import asyncio
import datetime
from typing import List
from w1thermsensor import AsyncW1ThermSensor, Unit, Sensor, W1ThermSensorError
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Z_WH.tools.meta import MetaData
from .notification import NotificationManager, Notification
from .displaymanager import DisplayManager, Slide, DISPLAY_SIZE
from .user import UserManager
from Z_WH.tools.log import Logger

logger = Logger('temp-sensor', 'temp')


(
    ERROR_SENSOR_NOT_FOUND,
    ERROR_SENSOR_IS_ALIVE,
    ERROR_SENSOR_NOT_ALIVE
) = (
    'SENSOR_NOT_FOUND',
    'SENSOR_IS_ALIVE',
    'SENSOR_NOT_ALIVE'
)


class TempSensorManagerError(Exception):
    def __init__(self, error: str):
        self.error: str = error


class ThermSensor:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name: str = kwargs.get('name')
        self.alive: bool = kwargs.get('alive')
        self.color: str or None = kwargs.get('color')
        self.displayOnScreen: bool = True if kwargs.get('displayOnScreen') is None else kwargs.get('displayOnScreen')

        self._temp: float = 0
        self.lastGettingTemp: datetime.datetime or None = None
        self.slide: Slide = Slide(duration=2)

    def init(self):
        self.slide.newId()
        self.flushSlide()

    # Reload the temperature
    async def refreshTemp(self):
        try:
            sensor = AsyncW1ThermSensor(Sensor.DS18B20, self.id)
            temp = round(await sensor.get_temperature(Unit.DEGREES_C), 2)
            self.alive = True
            if self._temp != temp:
                logger.temp(f'Sensor with id {sensor.id} is at {temp}°C')
                self.flushSlide()
            self._temp = temp
            self.lastGettingTemp = datetime.datetime.now()
        except W1ThermSensorError:
            self.alive = False
            if self.alive:
                self.slide.enable = False

    # Get the temperature
    def getTemp(self) -> float:
        return self._temp

    # Get the information about the sensor
    def getInfo(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'alive': self.alive,
            'displayOnScreen': self.displayOnScreen
        }

    def flushSlide(self):
        image = Image.new('1', DISPLAY_SIZE)
        draw = ImageDraw.Draw(image)
        ImageFont.load_default()
        draw.text(
            (3, 5),
            f"{self.name} : {int(self._temp)}°C",
            font=ImageFont.truetype('Z_WH/assets/font/coolvetica.ttf', 16),
            fill=255
        )
        self.slide.image = image


class TempSensorManager:
    def __init__(
            self,
            notificationManager: NotificationManager,
            displayManager: DisplayManager,
            userManager: UserManager
    ):
        self._notificationManager = notificationManager
        self._displayManager = displayManager
        self._userManager = userManager

        self._sensors: List[ThermSensor] = []

        self._refreshAliveSensorThread = None
        self._refreshTempSensorThread = None

        self._metaSensors = MetaData('temp-sensor')

    # Init the temp sensors
    def init(self):
        self._loadMetaSensors()
        self._refreshAliveSensor()
        asyncio.run(self._refreshTempSensor())

    # Load the sensors from meta
    def _loadMetaSensors(self):
        metaSensors = self._metaSensors.data
        if metaSensors:
            for metaSensor in metaSensors:
                sensor = ThermSensor(**metaSensor)
                sensor.init()
                if sensor.displayOnScreen and sensor.alive:
                    self._displayManager.addSlide(sensor.slide)
                self._sensors.append(sensor)

    # Save the meta data
    def _saveMetaSensors(self):
        self._metaSensors.data = [sensor.getInfo() for sensor in self._sensors]

    # Refresh temperature and alive sensor each 2 seconds
    def _refreshAliveSensor(self):
        self._refreshAliveSensorThread = threading \
            .Timer(5, lambda: self._refreshAliveSensor()) \
            .start()

        mustSaveMeta = False
        for aliveSensor in AsyncW1ThermSensor.get_available_sensors():
            try:
                self.getSensorById(aliveSensor.id)
            except TempSensorManagerError:
                sensor = ThermSensor(
                    id=aliveSensor.id,
                    name=f"@{aliveSensor.id[:5]}",
                    alive=True,
                    displayOnScreen=True
                )
                logger.info(f"New sensor detected with id {sensor.id}")
                sensor.init()
                self._sensors.append(sensor)
                if sensor.displayOnScreen and sensor.alive:
                    self._displayManager.addSlide(sensor.slide)
                mustSaveMeta = True
        if mustSaveMeta:
            self._saveMetaSensors()

    async def _refreshTempSensor(self):
        self._refreshTempSensorThread = threading\
            .Timer(2, lambda: asyncio.run(self._refreshTempSensor()))\
            .start()

        saveMeta = False
        for sensor in self._sensors:
            wasAlive = sensor.alive
            await sensor.refreshTemp()
            if wasAlive != sensor.alive:
                saveMeta = True
                notification = Notification()
                notification.subject = 'Z-WH sondes températures'
                if sensor.alive:
                    logger.info(f"Sensor with id {sensor.id} reconnect")
                    notification.content = f"La sonde de température {sensor.name} a été reconnectée !"
                else:
                    logger.warning(f"Sensor with id {sensor.id} is out of order")
                    notification.content = f"La sonde de température {sensor.name} a été déconnectée !"
                notification.email = self._userManager.email
                self._notificationManager.sendNotificationMail(notification)

        if saveMeta:
            self._saveMetaSensors()

    # Find a sensor with his id
    def getSensorById(self, sensor_id) -> ThermSensor:
        for sensor in self._sensors:
            if sensor.id == sensor_id:
                return sensor
        raise TempSensorManagerError(ERROR_SENSOR_NOT_FOUND)

    # Update the sensor information
    def sensorUpdate(self, sensorId: str, **kwargs):
        color = kwargs.get('color')
        name = kwargs.get('name')
        displayOnScreen = kwargs.get('displayOnScreen')
        sensor = self.getSensorById(sensorId)
        if color:
            sensor.color = color
        if name:
            assert len(name) <= 6, TempSensorManagerError('Name must be 6 length max !')
            sensor.name = name
        if displayOnScreen is not None:
            if not displayOnScreen:
                sensor.slide.enable = False
            elif sensor.alive:
                self._displayManager.addSlide(sensor.slide)
            sensor.displayOnScreen = displayOnScreen
        if color or name or displayOnScreen:
            self._saveMetaSensors()

    # Update many sensor information
    def sensorUpdateMany(self, updatedThermSensors: List[ThermSensor]):
        def getUpdatedSensor(sensorId: str) -> ThermSensor or None:
            for updatedThermSensor in updatedThermSensors:
                if updatedThermSensor.id == sensorId:
                    return updatedThermSensor
            return None

        # Check if id exist before update
        [self.getSensorById(updatedThermSensor.id) for updatedThermSensor in updatedThermSensors]

        for i in range(len(self._sensors)):
            updateSensor = getUpdatedSensor(self._sensors[i].id)
            if updateSensor:
                self._sensors[i] = updateSensor
        self._saveMetaSensors()

    # Delete out of order sensor
    def deleteOutOfOrderSensor(self, sensorId: str):
        for i in range(len(self._sensors)):
            currentSensor = self._sensors[i]
            if currentSensor.id == sensorId:
                if not currentSensor.alive:
                    self._sensors.pop(i)
                    self._saveMetaSensors()
                    return
                else:
                    raise TempSensorManagerError(ERROR_SENSOR_IS_ALIVE)
        raise TempSensorManagerError(ERROR_SENSOR_NOT_FOUND)

    # Delete all out of order sensors
    def deleteAllOutOfOrderSensor(self):
        for i in range(len(self._sensors)):
            if not self._sensors[i].alive:
                self._sensors.pop(i)
        self._saveMetaSensors()

    # Get the temperature from the sensor by id
    def getTemp(self, sensorId: str) -> float:
        return self.getSensorById(sensorId).getTemp()

    # Get sensor name
    def getName(self, sensorId: str) -> str:
        return self.getSensorById(sensorId).name

    # Get all sensor id
    def getAliveSensorsId(self) -> List[str]:
        return [sensor.id for sensor in self._sensors if sensor.alive]

    # Get sensors info
    def getSensorsInfo(self):
        return [sensor.getInfo() for sensor in self._sensors]
