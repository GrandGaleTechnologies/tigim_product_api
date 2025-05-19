from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.core.database import DBBase


class Store(DBBase):
    """
    Database model for stores
    """

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(
        String(20), ForeignKey("clients.client_id", ondelete="CASCADE"), nullable=False
    )
    type = Column(String(20), nullable=False)
    api_key = Column(String, nullable=False, comment="Encrypted Key")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
