from typing import List, Optional
from datetime import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from upload_service.db.dependencies import get_db_session
from upload_service.db.models.uploaded_file import UploadedFile


class UploadedFileDAO:
    """Class for accessing the uploaded files table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_uploaded_file(
        self,
        name: str,
        description: Optional[str],
        file_path: str,
        file_size: float,
        file_type: str,
    ) -> None:
        """
        Add a single uploaded file to the session.

        :param name: Name of the file.
        :param description: Optional description of the file.
        :param file_path: File storage path.
        :param file_size: Size of the file.
        :param file_type: MIME type or file extension.
        """
        uploaded_file = UploadedFile(
            name=name,
            description=description,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            created_at=datetime.utcnow(),
        )
        self.session.add(uploaded_file)

    async def get_all_files(self, limit: int, offset: int) -> List[UploadedFile]:
        """
        Get all uploaded files with limit/offset pagination.

        :param limit: Number of files to retrieve.
        :param offset: Starting index.
        :return: List of uploaded files.
        """
        raw_files = await self.session.execute(
            select(UploadedFile).limit(limit).offset(offset)
        )
        return list(raw_files.scalars().fetchall())

    async def filter_files(
        self,
        name: Optional[str] = None,
        file_type: Optional[str] = None,
    ) -> List[UploadedFile]:
        """
        Filter uploaded files by name, user ID, or file type.

        :param name: Name of the file.
        :param file_type: MIME type or file extension.
        :return: List of uploaded files matching the filter criteria.
        """
        query = select(UploadedFile)
        if name:
            query = query.where(UploadedFile.name == name)
        if file_type:
            query = query.where(UploadedFile.file_type == file_type)

        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
