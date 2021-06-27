import random
import string
import datetime as dt
from typing import List
from Z_WH.tools.meta import MetaData


class AutoTimeSlotManagerError(Exception):
    def __init__(self, message: str):
        self.message: str = message
        self.timeSlot: List[TimeSlot] = []


class TimeSlotError(Exception):
    def __init__(self, message: str):
        self.message = message


class TimeSlot:
    def __init__(self):
        self._id: str or None = None
        self.groupId: str or None = None
        self._start: dt.time = dt.time()
        self._end: dt.time = dt.time()

        self._idLength = 8

        self.setRandomId()

    def setRandomId(self):
        self._id = ''.join(map(
            lambda i: random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits),
            range(self._idLength)
        ))

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, timeSlotId: str):
        if len(timeSlotId) != self._idLength:
            raise ValueError('Time slot id must be 8 charts !')
        self._id = timeSlotId

    @property
    def startISO(self) -> str:
        return self._start.isoformat()

    @startISO.setter
    def startISO(self, ISOTime: str):
        self._start = dt.time.fromisoformat(ISOTime)

    @property
    def endISO(self) -> str:
        return self._end.isoformat()

    @endISO.setter
    def endISO(self, ISOTime: str):
        self._end = dt.time.fromisoformat(ISOTime)

    @classmethod
    def checkTime(cls, time: dt.time):
        if not isinstance(time, dt.time):
            raise TimeSlotError('Time must be datetime.time instance !')

    @property
    def start(self) -> dt.time:
        return self._start

    @start.setter
    def start(self, time: dt.time):
        self.checkTime(time)
        self._start = time

    @property
    def end(self) -> dt.time:
        return self._end

    @end.setter
    def end(self, time: dt.time):
        self.checkTime(time)
        self._end = time


class AutoTimeSlotManager:
    def __init__(self):
        self._timeSlots: List[TimeSlot] = []
        self._timeSlotsMeta = MetaData('time-slots')

    # Init the auto time slot manager
    def init(self):
        self.loadMetaTimeSlot()

    # Load the time slot from the meat data
    def loadMetaTimeSlot(self):
        metaSlots = self._timeSlotsMeta.data
        if metaSlots:
            for metaSlot in metaSlots:
                timeSlot = TimeSlot()
                timeSlot.id = metaSlot['id']
                timeSlot.startISO = metaSlot['start']
                timeSlot.endISO = metaSlot['end']
                timeSlot.groupId = metaSlot['groupId']
                self._timeSlots.append(timeSlot)

    # Save meta
    def saveMetaTimeSlots(self):
        self._timeSlotsMeta.data = [
            {
                'id': timeSlot.id,
                'groupId': timeSlot.groupId,
                'start': timeSlot.startISO,
                'end': timeSlot.endISO
            }
            for timeSlot in self._timeSlots
        ]

    # Get the current group id to enable for the auto mode
    def groupEnableNow(self) -> int or None:
        now = dt.datetime.now()
        time = dt.time(now.hour, now.minute, now.second)
        for timeSlot in self._timeSlots:
            if timeSlot.start <= time < timeSlot.end:
                return timeSlot.groupId
        return None

    # Check and update or add the time slots
    def addUpdateTimeSlot(self, newSlots: List[TimeSlot]):

        checkSlots = newSlots.copy()

        for currentSlot in self._timeSlots:
            if currentSlot.id not in [slot.id for slot in newSlots if slot.id]:
                checkSlots.append(currentSlot)

        checkSlots.sort(key=lambda slot: slot.start)

        for i in range(len(checkSlots)):
            checkSlot = checkSlots[i]
            if checkSlot.start >= checkSlot.end:
                error = AutoTimeSlotManagerError('START_END_INVALID')
                error.timeSlot = [checkSlot]
                raise error

            if i > 0:
                previousSlot = checkSlots[i - 1]
                if previousSlot.end >= checkSlot.start:
                    error = AutoTimeSlotManagerError('SLOT_MISS_MATCH')
                    error.timeSlot = [previousSlot, checkSlot]
                    raise error

        self._timeSlots = checkSlots
        self.saveMetaTimeSlots()

    # Delete slot
    def deleteTimeSlot(self, slotId: int):
        for i in range(len(self._timeSlots)):
            if self._timeSlots[i].id == slotId:
                self._timeSlots.pop(i)
                self.saveMetaTimeSlots()
                return
        raise AutoTimeSlotManagerError('Slot not found !')

    # Get all time slot
    def getTimeSlot(self):
        return self._timeSlots
