from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pathlib import Path


engine = create_engine(
    f"sqlite:///{Path(__file__).parent.parent.parent/Path('database_instances')/Path('database_telebot.db')}"
)

LocalSession = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
db = LocalSession()
