from sqlalchemy import Column, Integer, ForeignKey, TIME
from .base_entity import BaseEntity


class TimeSlot(BaseEntity):
    __tablename__ = 'time_slot'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('output_group.id'), nullable=False)
    start = Column(TIME, nullable=False)
    end = Column(TIME, nullable=False)
