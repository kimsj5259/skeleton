from typing import Optional, List
from datetime import datetime, date

from pydantic import EmailStr
from sqlmodel import (
    Field,
    SQLModel,
    Relationship,
)

from ...core.base_model import BaseIDModel
from ..schemas.user import GenderEnum


class UserBase(SQLModel):
    name: str = Field(nullable=False)
    email: EmailStr = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    gender: GenderEnum | None = Field(default=GenderEnum.other, nullable=True)
    birth_date: date | None = Field(nullable=True)
    is_active: bool = Field(default=True)

    updated_at: datetime | None = Field(default_factory=datetime.now)

    terms_of_use_agreement: bool = Field(default=False)
    use_of_information_agreement: bool = Field(default=False)


class User(BaseIDModel, UserBase, table=True):
    __tablename__ = "user"



class ProfileBase(SQLModel):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", unique=True)
    nickname: str | None = Field(nullable=True, unique=True)
    address: str | None = Field(nullable=True)
    profile_image: str | None = Field(nullable=True)
    updated_at: datetime | None = Field(default_factory=datetime.now)


class Profile(BaseIDModel, ProfileBase, table=True):
    __tablename__ = "profile"

    user: Optional[User] = Relationship(back_populates="profile")


