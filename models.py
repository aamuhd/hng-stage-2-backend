from sqlmodel import SQLModel, Field
import uuid
from uuid6 import uuid7
from datetime import datetime

from utils import get_utc_timestamp



class ProfileBase(SQLModel):
    name: str = Field(unique=True, index=True)
    gender: str
    gender_probability: float
    sample_size: int
    age: int
    age_group: str
    country_id: str
    country_probability: float


class ProfilePublic(SQLModel):
    id: uuid.UUID 
    name: str = Field(unique=True, index=True)
    gender: str
    gender_probability: float
    sample_size: int
    age: int
    age_group: str
    country_id: str
    country_probability: float
    created_at: datetime


class ProfileCreateResponse(SQLModel):
    status: str = "success"
    data: ProfilePublic


class ProfilesPublic(ProfileBase):
    status: str = "success"
    count: int
    data: list[ProfilePublic]


class ProfilesPublicResponse(SQLModel):
    status: str = "success"
    count: int
    data: list[ProfilePublic]



class Profile(ProfileBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid7, primary_key=True)
    created_at: datetime = Field(default_factory=get_utc_timestamp)



