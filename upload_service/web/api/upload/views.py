from fastapi import APIRouter
from typing import Union
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


from upload_service.db.dao.uploaded_file_dao import UploadedFileDAO
from upload_service.db.dependencies import get_db_session
from upload_service.utils.s3_utils import save_file_to_s3


router = APIRouter()

@router.post("/upload-file", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
    s3_bucket: str = 'spine-interview-bucket'
) -> Union[dict, JSONResponse]:
    """
    Upload a file to S3 and create a record in the database.

    :param file: The uploaded file.
    :param session: Database session (injected).
    :param file_dao: Data Access Object for file operations (injected).
    :param s3_bucket: Name of the S3 bucket.
    :return: JSON response message.
    """
    try:

        file_path = f"uploads/{file.filename}"
        content = await file.read()

        # file_url = save_file_to_s3(s3_bucket, file_path, content)
        uploaded_file_dao = UploadedFileDAO(session)
        await uploaded_file_dao.create_uploaded_file(
            name=file.filename,
            description=None,
            file_path=file_path,
            file_size=len(content) / (1024 * 1024),
            file_type=file.content_type,
        )
        await session.commit()

        return JSONResponse(content={'message': 'File uploaded and record created successfully'}, status_code=status.HTTP_201_CREATED)

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to upload file: {str(e)}")
