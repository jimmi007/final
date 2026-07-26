import logging
import tempfile

import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, status
from storeapi.libs.b2 import b2_upload_file

logger = logging.getLogger(__name__)

router = APIRouter()

CHUNK_SIZE = 1024 * 1024


@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile):
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            filename = temp_file.name
            logger.info(f"Saving uploaded file temporarily to {filename}")
            async with aiofiles.open(filename, "wb") as f:
                while chunk := await file.read(CHUNK_SIZE):
                    await f.write(chunk)

            file_url = b2_upload_file(local_file=filename, file_name=file.filename)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="There was an error uploading the file",
        )

    return {"detail": f"Successfully uploaded {file.filename}", "file_url": file_url}

# 1.Ποστάρει αρχείο ο χρήστης Upload file
# 2.Δημιουργείται temp_file με μέθοδο Named…που θα έχει το όνομα filename
# 3.Διαβάζει τα chunk από το Upload file,και τα γράφει στο filename.o f είναι ο φάκελος που λαμβάνει το
# 3.Διαβάζει τα chunk από το Upload file,και τα γράφει στο temp_file.
# 4.Παίρνει το temp_file(filename) και και το όνομα του και το ανεβάζει στο b2(cloud) και επιστρέφει ιστοσελίδα