from pydantic import BaseModel
from datetime import datetime
import uuid


class ContractBase(BaseModel):
    filename: str
    file_url: str

class ContractCreate(ContractBase):
    pass


class ContractOut(ContractBase):
    id: uuid.UUID
    upload_date: datetime

    class Config:
        orm_mode = True # Needed so Pydantic can read SQLAlchemy objects