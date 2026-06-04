from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    hubspot_id = Column(String, primary_key=True, index=True)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
