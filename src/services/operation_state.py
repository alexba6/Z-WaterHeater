import datetime
import threading
from src.utils.output import group_manager
from .auto import AutoTimeSlot

from ..tools.meta import MetaData

AUTO_MODE, MANUEL_MODE = 'auto', 'manuel'


class OperationState:
    def __init__(self):
        self._mode = AUTO_MODE
        self._start_auto_timer = None
        self._auto_timer = None

        self._meta = MetaData('operation-state')

        self._autoTimeSlot = AutoTimeSlot()
        self._autoTimeSlot.load()

    # Load the operation state
    def load(self):
        now = datetime.datetime.now().microsecond

        def start_auto_check():
            self._auto_check()

        threading.Timer(1 - (now / 10**6), start_auto_check).start()

        if self._meta.data is None:
            self._meta.data = {
                'auto_callback': 5
            }

    # Check each second the auto state
    def _auto_check(self):
        self._auto_timer = threading.Timer(1, self._auto_check)
        self._auto_timer.start()
        if self._mode != AUTO_MODE:
            return
        group_id = self._autoTimeSlot.groupToSwitchOn()
        if group_id:
            group_manager.switchOn(group_id)
        else:
            group_manager.switchOff()

    # Turn auto mode after a few time
    def _start_auto_callback(self):
        self._mode = MANUEL_MODE

        def callback():
            self._mode = AUTO_MODE

        auto_callback_config = self._meta.data.get('auto_callback')

        if auto_callback_config is not None:
            print(f'AUTO >>>>> {auto_callback_config}')
            self._start_auto_timer = threading.Timer(auto_callback_config, callback)
            self._start_auto_timer.start()

    # Switch on a group
    def switchOn(self, group_id: str):
        self._start_auto_callback()
        group_manager.switchOn(group_id)

    # Switch off a group
    def switchOff(self):
        self._start_auto_callback()
        group_manager.switchOff()

    # Switch auto
    def switchAuto(self):
        if self._start_auto_timer and self._start_auto_timer.is_alive():
            self._start_auto_timer.cancel()
        self._mode = AUTO_MODE


operation_sate = OperationState()
