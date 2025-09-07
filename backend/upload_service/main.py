from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from . import database, models, schemas, crud, storage
from typing import List


# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Upload Service")

# Dependency to inject DB session into endpoints
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload", response_model=schemas.ContractOut)
async def upload_contract(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF/DOCX allowed.")
    
    file_url = storage.save_file(file)

    contract_data = schemas.ContractCreate(filename=file.filename, file_url=file_url)
    db_contract = crud.create_contract(db, contract_data)
    return db_contract


@app.get("/contracts", response_model=List[schemas.ContractOut])
def list_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_contracts(db, skip=skip, limit=limit)

@app.get("/contracts/{contract_id}", response_model=schemas.ContractOut)
def get_contract(contract_id: UUID, db: Session = Depends(get_db)):
    contract = crud.get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@app.get("/health")
def health_check():
    return {"status": "ok"}


# run with uvicorn upload_service.main:app --reload to treat it as a package. Run this inside of backend dir