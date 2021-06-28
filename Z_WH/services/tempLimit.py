import asyncio
import threading
import schedule
from .tempSensor import TempSensorManager, TempSensorManagerError
from .notification import Notification, NotificationManager
from .user import UserManager
from Z_WH.tools.meta import MetaData


class TempLimitManager:
    def __init__(
            self,
            tempManager: TempSensorManager,
            notificationManager: NotificationManager,
            userManager: UserManager
    ):
        self._notificationManager = notificationManager
        self._userManager = userManager
        self._tempManager = tempManager
        self._meta = MetaData('temp-limit')
        self._sensorId: str or None = None
        self._limitTemp: float = 60
        self._tempDelta: float = 5

        self.isEnable: bool = False

        self._sendNotification: bool = True
        self._alreadySendNotification: bool = False

        self.changeStateCallback = None

    def init(self):
        self.loadMeta()

        def callback():
            self._alreadySendNotification = False
        schedule.every(1).day.at('00:00:00').do(lambda: callback())
        asyncio.run(self._checkIfEnable())

    def loadMeta(self):
        meta = self._meta.data
        if meta:
            self._sensorId = meta['sensorId']
            self._tempDelta = meta['tempDelta']
            self._limitTemp = meta['limitTemp']
            self._sendNotification = meta['sendNotification']

    def saveMeta(self):
        self._meta.data = {
            'sensorId': self._sensorId,
            'tempDelta': self._tempDelta,
            'limitTemp': self._limitTemp,
            'sendNotification': self._sendNotification
        }

    def sendTempAchievedNotification(self):
        if not self._alreadySendNotification:
            notification = Notification()
            notification.email = self._userManager.email
            notification.subject = 'Température limite atteinte'
            notification.content = f"La température limite de {self._limitTemp}°C a été atteinte !"
            self._notificationManager.sendNotificationMail(notification)
            self._alreadySendNotification = True

    async def _checkIfEnable(self):
        threading \
            .Timer(60, lambda: asyncio.run(self._checkIfEnable())) \
            .start()

        if self._sensorId is None:
            self.isEnable = True
            return
        try:
            temp = await self._tempManager.getTemp(self._sensorId)
        except TempSensorManagerError:
            return True
        if not self.isEnable:
            temp += self._tempDelta
        isEnable = temp <= self._limitTemp
        if self.isEnable != isEnable and self.changeStateCallback:
            if isEnable:
                self.sendTempAchievedNotification()
            self.changeStateCallback(isEnable)
        self.isEnable = isEnable
