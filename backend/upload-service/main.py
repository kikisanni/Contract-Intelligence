from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, schemas, crud


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
    
    # Fake storage path, we will use S3/local storage later
    file_url = f"/fake_storage/{file.filename}"

    contract_data = schemas.ContractCreate(filename=file.filename, file_url=file_url)
    db_contract = crud.create_contract(db, contract_data)
    return db_contract


# run with fastapi dev backend/upload_service/main.py --app upload_service.main:app to treat it as a package