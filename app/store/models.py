from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String

from app.core.database import DBBase


class Store(DBBase):
    """
    Database model for stores
    """

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(
        Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)
    auth_keys = Column(JSON(none_as_null=True), nullable=False, comment="Credentials")
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
