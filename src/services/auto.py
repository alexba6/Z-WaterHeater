import datetime as dt
from typing import List
from ..models.TimeSlot import TimeSlot
from ..config.database import Session


class AutoTimeSlot:
    def __init__(self):
        self._time_slots: List[TimeSlot] = []

    def load(self):
        with Session() as session:
            self._time_slots = session.query(TimeSlot).all()

    def groupToSwitchOn(self) -> int or None:
        now = dt.datetime.now()
        for slots in self._time_slots:
            # print(slots.start, dt.time(now.hour, now.minute, now.second), slots.end)
            if slots.start <= dt.time(now.hour, now.minute, now.second) < slots.end:
                return slots.group_id
        return None
