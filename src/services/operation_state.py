import datetime
import threading
from src.utils.output import groupManager
from .auto import AutoTimeSlot

from ..tools.meta import MetaData

AUTO_MODE, ON, OFF = 'auto', 'on', 'off'


class OperationState:
    def __init__(self):
        self._mode = AUTO_MODE
        self._currentGroupOn = None

        self._autoCallBackTime: float = 60*60*12

        self._autoStartTimer = None
        self._autoCheckTimer = None

        self._meta = MetaData('operation-state')

        self._autoTimeSlot = AutoTimeSlot()

        self._autoGroupId = None

    # Load the operation state
    def init(self):
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
        self._autoGroupId = self._autoTimeSlot.groupToSwitchOn()
        if self._autoGroupId:
            groupManager.switchOn(self._autoGroupId)
        else:
            groupManager.switchOff()

    # Turn auto mode after a few time
    def startAutoCallBack(self, mode: str):
        def callback():
            if self._autoCallBackTime > 0:
                self._mode = AUTO_MODE
                self._currentGroupOn = None
        self._mode = mode
        self._autoStartTimer = threading.Timer(self._autoCallBackTime, callback)
        self._autoStartTimer.start()

    # Switch on a group
    def switchOn(self, group_id: str):
        self.startAutoCallBack(ON)
        self._currentGroupOn = group_id
        groupManager.switchOn(group_id)

    # Switch off a group
    def switchOff(self):
        self.startAutoCallBack(OFF)
        self._currentGroupOn = None
        groupManager.switchOff()

    # Switch auto
    def switchAuto(self):
        if self._autoStartTimer and self._autoStartTimer.is_alive():
            self._autoStartTimer.cancel()
        self._currentGroupOn = None
        self._mode = AUTO_MODE

    # Get the current mode
    def getMode(self):
        return {
            'mode': self._mode,
            'onGroup': self._currentGroupOn
        }


operation_sate = OperationState()
