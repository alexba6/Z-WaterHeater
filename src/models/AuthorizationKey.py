from sqlalchemy import Column, Integer, String, Text, ForeignKey, DATETIME

from .base_entity import BaseEntity
from ..tools import random_key


class AuthorizationKey(BaseEntity):
    __tablename__ = 'authorization_keys'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(50), nullable=True)
    key = Column(Text, nullable=False)
    user_agent = Column(String(255), nullable=True)
    last_generated = Column(DATETIME(), nullable=False)
    created_at = Column(DATETIME(), nullable=False)

    def match_key(self, key):
        return self.key == key

    def generate_key(self, length=250):
        key = random_key.generate_key(length)
        self.key = key
        return key
