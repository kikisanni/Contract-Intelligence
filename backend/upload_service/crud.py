from sqlalchemy.orm import Session
from uuid import UUID
from . import models, schemas


def create_contract(db: Session, contract: schemas.ContractCreate):
    db_contract = models.Contract(
        filename = contract.filename,
        file_url = contract.file_url
    )

    db.add(db_contract)
    db.commit()
    db.refresh(db_contract) # fetch back with ID + upload_date
    return db_contract

def get_contracts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contract).offset(skip).limit(limit).all()

def get_contract_by_id(db: Session, contract_id: UUID):
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()