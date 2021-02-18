import datetime
import time
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
DeclarativeBase = declarative_base()
 
class Test(DeclarativeBase):
    __tablename__ = 'test'
 
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
 
# Prepare database and session
 
engine = create_engine('sqlite://', echo=False)
DeclarativeBase.metadata.create_all(engine)
session_maker = sessionmaker(engine)
session = session_maker()
 
# Test
 
t = Test()
session.add(t)
session.flush()
 
time.sleep(1)
 
t2 = Test()
session.add(t2)
session.flush()
 
print(t.created)
print(t2.created)