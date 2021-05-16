from .User import User
from .AuthorizationKey import AuthorizationKey
from ..config.database import engine
from .base_entity import BaseEntity


def create_all_table():
    print('Creating all tables...')
    BaseEntity.metadata.create_all(engine)
