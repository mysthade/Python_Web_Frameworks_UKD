import shutil
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, status

from core.handlers import run_handler

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(
    path="/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file to the server",
)
async def upload_file(file: UploadFile = File(...)):
    async def handler():
        upload_dir = Path("uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_location = upload_dir / f"uploaded_{file.filename}"
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"info": f"File '{file.filename}' saved at '{file_location}'"}

    try:
        return await run_handler(
            handler,
            log_message="Failed to upload file",
            error_detail="Could not upload file",
        )
    finally:
        await file.close()
