import os

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_USER = os.environ["DB_USER"]
DB_NAME = os.environ["DB_NAME"]

Base = declarative_base()
engine = create_engine(
    f"postgresql://{DB_USER}@localhost/{DB_NAME}",
    echo=False,
    execution_options={"isolation_level": "READ COMMITTED"},
)
Session = sessionmaker(bind=engine)


class WorkCoverageRecord(Base):
    __tablename__ = "workcoveragerecords"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), index=True)
