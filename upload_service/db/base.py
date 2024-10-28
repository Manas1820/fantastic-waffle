from sqlalchemy.orm import DeclarativeBase

from upload_service.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
