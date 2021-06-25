import datetime as dt
from typing import List
from Z_WH.models.TimeSlot import TimeSlot
from Z_WH.config.database import Session


class AutoTimeSlotManagerError(Exception):
    def __init__(self, message: str):
        self.message: str = message
        self.timeSlot: List[TimeSlot] = []


class AutoTimeSlotManager:
    def __init__(self):
        self._timeSlots: List[TimeSlot] = []

    # Init the auto time slot manager
    def init(self):
        self.loadTimeSlot()

    # Load the time slot from the database
    def loadTimeSlot(self):
        with Session() as session:
            self._timeSlots = session.query(TimeSlot).all()

    # Get the current group id to enable for the auto mode
    def groupEnableNow(self) -> int or None:
        now = dt.datetime.now()
        time = dt.time(now.hour, now.minute, now.second)
        for timeSlot in self._timeSlots:
            if timeSlot.start <= time < timeSlot.end:
                return timeSlot.group_id
        return None

    # Check and update or add the time slots
    def addUpdateTimeSlot(self, newSlots: List[TimeSlot]):

        checkSlots = newSlots.copy()

        for currentSlot in self._timeSlots:
            if currentSlot.id not in [slot.id for slot in newSlots]:
                checkSlots.append(currentSlot)

        checkSlots.sort(key=lambda slot: slot.start)

        for i in range(len(checkSlots)):
            checkSlot = checkSlots[i]
            if checkSlot.start <= checkSlot.end:
                error = AutoTimeSlotManagerError('START_END_INVALID')
                error.timeSlot = [checkSlot]
                raise AutoTimeSlotManagerError('START_END_INVALID')

            if i < 0:
                previousSlot = checkSlots[i - 1]
                if previousSlot.end > checkSlot.start:
                    error = AutoTimeSlotManagerError('SLOT_MISS_MATCH')
                    error.timeSlot = [previousSlot, checkSlot]

        with Session() as session:
            for newSlot in newSlots:
                session.add(newSlot)
            session.commit()

        self._timeSlots = checkSlots

    # Delete slot
    def deleteTimeSlot(self, slotId: int):
        with Session as session:
            slot = session.query(TimeSlot) \
                .filter(TimeSlot.id == slotId) \
                .first()
            if not slot:
                raise AutoTimeSlotManagerError('GROUP_NOT_FOUND')
            session.delete(slot)
            session.commit()
            for i in range(len(self._timeSlots)):
                if self._timeSlots[i] == slotId:
                    self._timeSlots.pop(i)
                    break


autoTimeSlotManager = AutoTimeSlotManager()
