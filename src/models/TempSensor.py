from sqlalchemy import Column, Integer, ForeignKey, TIME, String
from .base_entity import BaseEntity


class TempSensor(BaseEntity):
    __tablename__ = 'temp_sensor'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String(30), nullable=False)
    name = Column(String(255), nullable=True)
