from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import DBBase


class Client(DBBase):
    """
    Database model for clients
    """

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String(20), unique=True, nullable=False)
    hashed_secret = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
