import logging
import tempfile

import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, status
from storeapi.libs.b2 import b2_upload_file

logger = logging.getLogger(__name__)

router = APIRouter()

CHUNK_SIZE = 1024 * 1024



import os
import tempfile

@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        filename = temp_file.name
        temp_file.close()

        logger.info(f"Saving uploaded file temporarily to {filename}")

        async with aiofiles.open(filename, "wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)

        file_url = b2_upload_file(local_file=filename, file_name=file.filename)

        os.remove(filename)

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return {
        "detail": f"Successfully uploaded {file.filename}",
        "file_url": file_url
    }