from fastapi import Query
from sqlmodel import SQLModel, Field
from typing import Literal, Annotated



# Use Annotated for constraints (recommended in Pydantic v2 + FastAPI)
PositiveInt = Annotated[int, Field(ge=0)]
PositiveFloat = Annotated[float, Field(ge=0.0, le=1.0)]



class ProfileFilters(SQLModel):
    gender: str | None = None
    age_group: str | None = None
    country_id: str | None = None
    min_age: PositiveInt | None = None
    max_age: PositiveInt | None = None
    min_gender_probability: PositiveFloat | None = None
    min_country_probability: PositiveFloat | None = None
    sort_by: Literal["age", "created_at", "gender_probability"] | None = None
    order: Literal["asc", "desc"] = "asc"
    #page: int = Field(1, ge=1)
    #limit: int = Field(10, ge=1, le=50)
    page: int = Query(1, ge=1, description="Page number")
    limit: int = Query(
        10, 
        ge=1, 
        le=50, 
        description="Number of items per page (max 50)"
    )

    def get_offset(self) -> int:
        return (self.page - 1) * self.limit