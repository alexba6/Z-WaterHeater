import datetime
import threading
from typing import List
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


from ..tools.meta import MetaData

from ..models.TimeSlot import TimeSlot
from ..config.database import Session
from ..utils.output import groupManager
from .display import display


ON, OFF, AUTO = 'on', 'off', 'auto'


class OutManagerError(Exception):
    def __init__(self, message: str):
        self.message = message


class OutManager:
    def __init__(self):
        self.mode: str = AUTO
        self.enableGroupId: int or None = None

        self._autoCheckTimer = None
        self._autoStartTimer = None

        self._autoStartTime: float = 60*60*12

        self._timeSlots: List[TimeSlot] = []

        self._meta = MetaData('out-manager')

        self._screen()

    def init(self):
        self.loadMeta()
        self.loadTimeSlot()

    # Load the meta data
    def loadMeta(self):
        if self._meta.data:
            autoStartTime = self._meta.data.get('autoStartTime')
            if autoStartTime:
                self._autoStartTime = autoStartTime

    # Load the time slots
    def loadTimeSlot(self):
        with Session() as session:
            self._timeSlots = session.query(TimeSlot).all()

    # Check the output group for the auto mode
    def _autoThread(self):
        self._autoCheckTimer = threading.Timer(1, lambda: self._autoThread())
        self._autoCheckTimer.start()

        now = datetime.datetime.now()
        time = datetime.time(now.hour, now.minute, now.second)

        def getGroupId() -> int or None:
            for timeSlot in self._timeSlots:
                if timeSlot.start <= time < timeSlot.end:
                    return timeSlot.group_id
            return None

        groupIp = getGroupId()
        if self.enableGroupId == groupIp:
            return
        if groupIp:
            groupManager.switchOn(groupIp)
        else:
            groupManager.switchOff()
        self.enableGroupId = groupIp

    # Switch the group
    def switch(self, mode: str, groupId: int = None):
        if mode == self.mode:
            return
        if mode not in [ON, OFF, AUTO]:
            raise OutManagerError('Invalid mode')

        def stopTimer():
            if self._autoCheckTimer and self._autoCheckTimer.is_alive():
                self._autoCheckTimer.cancel()
            if self._autoStartTime and self._autoStartTimer.is_alive():
                self._autoStartTimer.cancel()

        if mode == ON:
            groupManager.switchOn(groupId)
            self.enableGroupId = groupId
        if mode == OFF:
            groupManager.switchOff()
            self.enableGroupId = None
        if mode == AUTO:
            stopTimer()
            self._autoThread()

        if mode in [ON, OFF]:
            stopTimer()
            self._autoStartTimer = threading.Timer(self._autoStartTime, lambda: self._autoThread())
            self._autoStartTimer.start()

        self.mode = mode

    # Display the current mode and enable group
    @display.addSlide(2)
    def _screen(self):
        text = self.mode.upper()
        if self.enableGroupId:
            text += ' : ' + groupManager.getGroup(self.enableGroupId).name
        image = Image.new('1', display.displaySize)
        draw = ImageDraw.Draw(image)
        ImageFont.load_default()
        font = ImageFont.truetype('src/assets/font/coolvetica.ttf', 32)
        draw.text((0, 0), text, font=font, fill=255)
        return image


outManager = OutManager()
