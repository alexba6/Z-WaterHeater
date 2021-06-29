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
from Z_WH.tools.log import logger

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

        self._sensor: AsyncW1ThermSensor or None = None
        self._temp: float = 0
        self.lastGettingTemp: datetime.datetime or None = None
        self.slide: Slide = Slide(duration=2)
        self._reloadTempThread: threading.Timer or None = None
        self.onOutOfOrderCallback = None

    def init(self):
        self.slide.newId()

    def start(self):
        if self._reloadTempThread and not self._reloadTempThread.is_alive():
            self._reloadTempThread()
        self.flushSlide()

    def stop(self):
        if self._reloadTempThread and self._reloadTempThread.is_alive():
            self._reloadTempThread.canncel()

    def reload(self):
        self.stop()
        self.start()

    # Reload the temperature
    async def _reloadTemp(self):
        timer = 2 if self.alive else 4
        self._reloadTempThread = threading\
            .Timer(timer, lambda: asyncio.run(self._reloadTemp()))\
            .start()
        try:
            temp = round(await self._sensor.get_temperature(Unit.DEGREES_C), 2)
            if self._temp != temp:
                self.flushSlide()
            self._temp = temp
            self.lastGettingTemp = datetime.datetime.now()
        except W1ThermSensorError:
            if self.alive:
                self.slide.enable = False
                logger.error(f"Temp sensor @{self.id} out of order")
                if self.onOutOfOrderCallback:
                    self.onOutOfOrderCallback()
            self.alive = False

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

        self._refreshSensorsThread = None

        self._metaSensors = MetaData('temp-sensor')

    # Init the temp sensors
    def init(self):
        self._loadMetaSensors()
        asyncio.run(self._refreshSensors())

    # Load the sensors from meta
    def _loadMetaSensors(self):
        metaSensors = self._metaSensors.data
        if metaSensors:
            for metaSensor in metaSensors:
                sensor = ThermSensor(**metaSensor)
                sensor.init()
                sensor.start()
                sensor.onOutOfOrderCallback = lambda: self._outOfOrderCallback(sensor)
                self._sensors.append(sensor)

    def _outOfOrderCallback(self, sensor: Sensor):
        notification = Notification()
        notification.subject = 'Z-WH sondes températures'
        notification.content = f"La sonde de température {sensor.name} a été déconnectée !"
        notification.email = self._userManager.email
        self._notificationManager.sendNotificationMail(notification)

    # Save the meta data
    def _saveMetaSensors(self):
        self._metaSensors.data = [sensor.getInfo() for sensor in self._sensors]

    # Refresh temperature and alive sensor each 2 seconds
    async def _refreshSensors(self):
        self._refreshSensorsThread = threading \
            .Timer(5, lambda: asyncio.run(self._refreshSensors())) \
            .start()

        mustSaveMeta = False
        for aliveSensor in AsyncW1ThermSensor.get_available_sensors():
            try:
                self.getSensorById(aliveSensor.id)
            except TempSensorManagerError:
                self._sensors.append(ThermSensor(
                    id=aliveSensor.id,
                    name=f"@{aliveSensor.id[:5]}",
                    alive=True,
                    displayOnScreen=True
                ))
                mustSaveMeta = True
        if mustSaveMeta:
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
