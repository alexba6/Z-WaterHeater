from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from os import makedirs, path

from . import DEBUG

DB_DIR = './data/db'

if not path.exists(DB_DIR):
    makedirs(DB_DIR, exist_ok=True)

load_dotenv()

Session = sessionmaker()

engine = create_engine(f'sqlite:///{DB_DIR}/data.db', echo=DEBUG)

Session.configure(bind=engine)
