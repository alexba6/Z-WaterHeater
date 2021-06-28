import asyncio
import threading
from .tempSensor import TempSensorManager, TempSensorManagerError
from Z_WH.tools.meta import MetaData


class TempLimitManager:
    def __init__(self, tempManager: TempSensorManager):
        self._tempManager = tempManager
        self._meta = MetaData('temp-limit')
        self._sensorId: str or None = None
        self._limitTemp: float = 60
        self._tempDelta: float = 5

        self.isEnable: bool = False

        self.changeStateCallback = None

    def init(self):
        self.loadMeta()

        asyncio.run(self._checkIfEnable())

    def loadMeta(self):
        meta = self._meta.data
        if meta:
            self._sensorId = meta['sensorId']
            self._tempDelta = meta['tempDelta']
            self._limitTemp = meta['limitTemp']

    def saveMeta(self):
        self._meta.data = {
            'sensorId': self._sensorId,
            'tempDelta': self._tempDelta,
            'limitTemp': self._limitTemp
        }

    async def _checkIfEnable(self):
        threading \
            .Timer(30, lambda: asyncio.run(self._checkIfEnable())) \
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
        print(f"Update temp: {temp}, limit : {self._limitTemp}, delta : {self._tempDelta} chauffage en marche: {not self.isEnable}")
        isEnable = temp <= self._limitTemp

        if self.isEnable != isEnable and self.changeStateCallback:
            self.changeStateCallback(isEnable)
        self.isEnable = isEnable
