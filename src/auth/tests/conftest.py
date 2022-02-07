from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth.database import Base
import os
import pytest


@pytest.fixture
def db():
    db_name = uuid4()
    db_url = f"sqlite:///./{db_name}.db"

    engine = create_engine(
        db_url, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        os.remove(f"{db_name}.db")
