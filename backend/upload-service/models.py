from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.timezone.utc)