from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Float
from datetime import datetime
from upload_service.db.base import Base


class UploadedFile(Base):
    """Model to store metadata and manage uploaded files."""

    __tablename__ = "uploaded_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200), nullable=False)
    description: Mapped[str] = mapped_column(String(length=500), nullable=True)
    file_path: Mapped[str] = mapped_column(String(length=300), nullable=False)
    file_size: Mapped[float] = mapped_column(Float, nullable=False)
    file_type: Mapped[str] = mapped_column(String(length=50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
