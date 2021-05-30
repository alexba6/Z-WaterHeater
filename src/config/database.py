from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from . import DEBUG

load_dotenv()

Session = sessionmaker()

engine = create_engine(getenv('DATABASE_URI'), echo=DEBUG)

Session.configure(bind=engine)
