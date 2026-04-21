from fastapi import Query
from sqlmodel import SQLModel, Field
from typing import Literal



class ProfileFilters(SQLModel):
    gender: str | None = None
    age_group: str | None = None
    country_id: str | None = None
    min_age: int | None = Field(default=None, ge=0)
    max_age: int | None = Field(default=None, ge=0)
    min_gender_probability: float | None = Field(default=None, ge=0.0, le=1.0)
    min_country_probability: float | None = Field(default=None, ge=0.0, le=1.0)
    sort_by: Literal["age", "created_at", "gender_probability"] | None = None
    order: Literal["asc", "desc"] = "asc"
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=50)

    def get_offset(self) -> int:
        return (self.page - 1) * self.limit