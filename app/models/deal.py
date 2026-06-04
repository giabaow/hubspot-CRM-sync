from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Deal(Base):
    __tablename__ = "deals"

    hubspot_id = Column(String, primary_key=True, index=True)
    dealname = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    dealstage = Column(String, nullable=True)
    closedate = Column(String, nullable=True)
    pipeline = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
