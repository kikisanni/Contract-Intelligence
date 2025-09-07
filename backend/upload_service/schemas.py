from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ContractBase(BaseModel):
    filename: str
    file_url: str

class ContractCreate(ContractBase):
    pass


class ContractOut(ContractBase):
    id: UUID
    upload_date: datetime

    class Config:
        from_attributes = True # Needed so Pydantic can read SQLAlchemy objects