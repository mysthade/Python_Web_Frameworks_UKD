import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file to the server",
)
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_dir = Path("uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_location = upload_dir / f"uploaded_{file.filename}"
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"info": f"File '{file.filename}' saved at '{file_location}'"}
    except Exception as exc:
        logger.exception("Failed to upload file")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not upload file",
        ) from exc
    finally:
        await file.close()
