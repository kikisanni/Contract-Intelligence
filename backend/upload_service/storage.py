import os
import shutil
import boto3
from fastapi import UploadFile
from dotenv import load_dotenv
from uuid import uuid4


load_dotenv()

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "./uploaded_files")

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


# Ensure local storage folder exists
if STORAGE_BACKEND == "local":
    os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)


def save_file(file: UploadFile) -> str:
    """
    Save file to local or S3, return file_url
    """

    file_id = str(uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    stored_filename = f"{file_id}{file_ext}"

    if STORAGE_BACKEND == "local":
        file_path = os.path.join(LOCAL_STORAGE_PATH, stored_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path
    
    elif STORAGE_BACKEND == "s3":
        s3 = boto3.client("s3", region_name=AWS_REGION)
        s3.upload_fileobj(file.file, S3_BUCKET, stored_filename)
        return f"s3://{S3_BUCKET}/{stored_filename}"
    
    else:
        raise ValueError(f"Unsupported storage backend: {STORAGE_BACKEND}")