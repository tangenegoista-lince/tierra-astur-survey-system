from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
import os
import shutil
from uuid import uuid4
from pathlib import Path

from app.core.config import settings
from app.core.database import get_db
from app.models.survey import Survey
from sqlalchemy.orm import Session

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_survey_card(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a survey card image and create a survey record.
    """
    # Validate file type (optional)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Allowed types: {allowed_extensions}"
        )

    # Generate a unique filename to avoid collisions
    unique_filename = f"{uuid4()}{file_ext}
    file_path = UPLOAD_DIR / unique_filename

    # Save the file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
    finally:
        file.file.close()

    # Create survey record
    db_survey = Survey(
        card_image_url=str(file_path),
        status="pending"
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Survey card uploaded successfully",
            "survey_id": str(db_survey.id),
            "filename": unique_filename,
            "file_path": str(file_path)
        }
    )