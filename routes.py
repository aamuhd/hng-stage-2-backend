from fastapi import APIRouter
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from sqlmodel import select, func, col

from deps import SessionDep
from models import Profile, ProfilesPublicResponse, ProfileCreateResponse
from api import get_data
import uuid



router = APIRouter()


class RequestBody(BaseModel):
    name: str


@router.post("/api/profiles", status_code=201, response_model=ProfileCreateResponse)
async def create_profile(request: RequestBody, session: SessionDep):

    if request.name is None or request.name.strip() == "":
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Missing or empty name parameter"
            }
        )
    
    if request.name.isdigit():
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Invalid type"
            }
        )
    
    # Get name from db
    statement = select(Profile).where(Profile.name == request.name)
    existing_profile = session.exec(statement).first()
    if existing_profile:
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Profile already exists",
                "data":{
                    "id": "b3f9c1e2-7d4a-4c91-9c2a-1f0a8e5b6d12",
                    "name": "ella",
                    "gender": existing_profile.gender,
                    "gender_probability": existing_profile.gender_probability,
                    "sample_size": existing_profile.sample_size,
                    "age": existing_profile.age,
                    "age_group": existing_profile.age_group,
                    "country_id": "DRC",
                    "country_probability": existing_profile.country_probability,
                    "created_at": existing_profile.created_at.isoformat().replace("+00:00", "Z")
                }
            }
        )
    
    data = await get_data(request.name)
    profile = Profile.model_validate(data, update={"name":request.name.lower()})
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {
        "data": profile
    }
    
    
@router.get("/api/profiles/{id}", response_model=ProfileCreateResponse)
def get_profile(id:uuid.UUID, session: SessionDep):
    profile = session.exec(select(Profile).where(Profile.id == id)).first()
    if profile is None:
        return JSONResponse(
            status_code=404,
            content={ "status": "error", "message": "Profile not found" }
        )
    return {
        "status": "success",
        "data": profile
    }


@router.get("/api/profiles", response_model=ProfilesPublicResponse)
def read_all_users(
    session: SessionDep,
    gender: str | None = None,
    country_id: str | None = None,
    age_group: str | None = None
):
    
    count_statement = select(func.count()).select_from(Profile)
    count = session.exec(count_statement).one()

    statement = select(Profile).order_by(col(Profile.created_at).desc())
    if gender:
        statement = statement.where(
            func.lower(Profile.gender) == gender.lower()
        )
    if country_id:
        statement = statement.where(
            func.lower(Profile.country_id) == country_id.lower()
        )
    if age_group:
        statement = statement.where(
            func.lower(Profile.age_group) == age_group.lower()
        )

    profiles = session.exec(statement).all()
    return {
        "status": "success",
        "count": count,
        "data": profiles
    }


@router.delete("/api/profiles/{id}", status_code=204)
def delete_profile(id: uuid.UUID, session: SessionDep):
    profile = session.exec(select(Profile).where(Profile.id == id)).first()
    if profile is None:
        return JSONResponse(
            status_code=404,
            content={ "status": "error", "message": "Profile not found" }
        )
    session.delete(profile)
    session.commit()
    return
    

