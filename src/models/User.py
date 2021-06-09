from sqlalchemy import Column, Integer, String, DATETIME
import datetime
import bcrypt
from .base_entity import BaseEntity

READER, WRITER, ADMIN = 'R', 'W', 'A'


class User(BaseEntity):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=False)
    password = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False)
    last_login = Column(DATETIME(), nullable=False)
    created_at = Column(DATETIME(), nullable=False)

    def __init__(self, email=None, username=None, password=None, role=None):
        date = datetime.datetime.now()
        self.created_at = date
        self.last_login = date
        self.email = email
        self.username = username
        self.hash_password(password)
        if role and not (role != READER or role != WRITER or role != ADMIN):
            raise Exception('Invalid role !')
        self.role = role

    def hash_password(self, password):
        passwd = bytes(password, encoding='utf-8')
        self.password = bcrypt.hashpw(passwd, bcrypt.gensalt(12))

    def verify_password(self, password):
        password = bytes(password, encoding='utf-8')
        return bcrypt.checkpw(password, self.password)
