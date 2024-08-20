from datetime import datetime

from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr

# from .utils.auth.uuid6 import uuid7, UUID


class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__


class BaseIDModel(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default_factory=datetime.now, nullable=True)
