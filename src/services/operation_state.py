import datetime
import threading
from src.utils.output import group_manager
from .auto import AutoTimeSlot

from ..tools.meta import MetaData

AUTO_MODE, MANUEL_MODE = 'auto', 'manuel'


class OperationState:
    def __init__(self):
        self._mode = AUTO_MODE

        self._autoCallBackTime: float = 60*60*12

        self._autoStartTimer = None
        self._autoCheckTimer = None

        self._meta = MetaData('operation-state')

        self._autoTimeSlot = AutoTimeSlot()

    # Load the operation state
    def load(self):
        self._autoTimeSlot.load()
        threading.Timer(
            1 - (datetime.datetime.now().microsecond / 10**6),
            lambda: self._autoCheck()
        ).start()

        if self._meta.data is None:
            self._meta.data = {
                'autoCallbackTime': self._autoCallBackTime
            }
        else:
            self._autoCallBackTime = self._meta.data.get('autoCallbackTime')

    # Get the operation state configuration
    def getConfig(self):
        return self._meta.data

    # Set the operation state configuration
    def saveConfig(self, **kwargs):
        if kwargs.get('autoCallbackTime'):
            self._autoCallBackTime = kwargs['autoCallbackTime']
        self.saveMeta()

    # Save the operation state meta
    def saveMeta(self):
        self._meta.data = {
            'autoCallbackTime': self._autoCallBackTime
        }

    # Check each second the auto state
    def _autoCheck(self):
        self._autoCheckTimer = threading.Timer(1, self._autoCheck)
        self._autoCheckTimer.start()

        if self._mode != AUTO_MODE:
            return
        group_id = self._autoTimeSlot.groupToSwitchOn()
        if group_id:
            group_manager.switchOn(group_id)
        else:
            group_manager.switchOff()

    # Turn auto mode after a few time
    def startAutoCallBack(self):
        def callback():
            print('AUTO MODE')
            self._mode = AUTO_MODE
        self._mode = MANUEL_MODE
        self._autoStartTimer = threading.Timer(self._autoCallBackTime, callback)
        self._autoStartTimer.start()

    # Switch on a group
    def switchOn(self, group_id: str):
        self.startAutoCallBack()
        group_manager.switchOn(group_id)

    # Switch off a group
    def switchOff(self):
        self.startAutoCallBack()
        group_manager.switchOff()

    # Switch auto
    def switchAuto(self):
        if self._autoStartTimer and self._autoStartTimer.is_alive():
            self._autoStartTimer.cancel()
        self._mode = AUTO_MODE


operation_sate = OperationState()
