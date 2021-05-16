from sqlalchemy import Column, Integer, String
import bcrypt
from .base_entity import BaseEntity

READER, WRITER = 'R', 'W'


class User(BaseEntity):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=False)
    password = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        role = kwargs.get('role')
        if role and role != READER and role != WRITER:
            raise Exception('Role must be reader or writter !')
        self.role = role if role else READER
        passwd = bytes(kwargs.get('password'), encoding='utf-8')
        self.password = bcrypt.hashpw(passwd, bcrypt.gensalt(12))

    def verify_password(self, password):
        password = bytes(password, encoding='utf-8')
        user_hash = bytes(self.password, encoding='utf-8')
        return bcrypt.checkpw(password, user_hash)
