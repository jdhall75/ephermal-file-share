import time

from sqlalchemy import Column, Integer, String

from .database import Base


class UploadFiles(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    key = Column(String, nullable=False, index=True)
    created = Column(Integer, default=int(time.time()), index=True)
