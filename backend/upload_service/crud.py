from sqlalchemy.orm import Session
from . import models, schemas


def create_contract(db: Session, contract: schemas.ContractCreate):
    db_contract = models.Contract(
        file_name = contract.filename,
        file_url = contract.file_url
    )

    db.add(db_contract)
    db.commit()
    db.refresh(db_contract) # fetch back with ID + upload_date
    return db_contract