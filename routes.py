from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse


from pydantic import BaseModel
from sqlmodel import select, func, col, desc, asc

from deps import SessionDep
from models import Profile, ProfilesPublicResponse, ProfileCreateResponse
from filters import ProfileFilters
from api import get_data
import uuid
from nl_parser import parse_natural_query



# helper function
def build_filtered_query(filters: ProfileFilters):
    query = select(Profile)

    if filters.gender:
        query = query.where(Profile.gender == filters.gender)
    if filters.age_group:
        query = query.where(Profile.age_group == filters.age_group)
    if filters.country_id:
        query = query.where(Profile.country_id == filters.country_id)
    if filters.min_age is not None:
        query = query.where(Profile.age >= filters.min_age)
    if filters.max_age is not None:
        query = query.where(Profile.age <= filters.max_age)
    if filters.min_gender_probability is not None:
        query = query.where(Profile.gender_probability >= filters.min_gender_probability)
    if filters.min_country_probability is not None:
        query = query.where(Profile.country_probability >= filters.min_country_probability)

    # Sorting
    if filters.sort_by:
        order_func = desc if filters.order == "desc" else asc
        query = query.order_by(order_func(getattr(Profile, filters.sort_by)))

    return query


router = APIRouter()


class RequestBody(BaseModel):
    name: str




@router.get("/api/profiles/search", response_model=ProfilesPublicResponse)
def search_profiles(
    session: SessionDep,
    q: str = Query(..., min_length=1),
    page: int = 1,
    limit: int = Query(10, ge=1, le=50)
):
    parsed = parse_natural_query(q)
    if not parsed:
        raise HTTPException(status_code=400, detail="Unable to interpret query")

    # Convert parsed dict to ProfileFilters
    filters = ProfileFilters(
        **parsed,
        page=page,
        limit=limit
    )

    query = build_filtered_query(filters)

    total = session.exec(select(func.count()).select_from(query.subquery())).one()
    offset = (page - 1) * limit
    results = session.exec(query.offset(offset).limit(limit)).all()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": results
    }
    



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


# Return all filtered profiles
@router.get("/api/profiles", response_model=ProfilesPublicResponse)
def read_all_users(
    session: SessionDep,
    filters: ProfileFilters = Depends()
):
    

    query = build_filtered_query(filters)

    # Count total
    total = session.exec(select(func.count()).select_from(query.subquery())).one()

    # Paginate
    offset = filters.get_offset()
    results = session.exec(query.offset(offset).limit(filters.limit)).all()
    return {
        "status": "success",
        "page": filters.page,
        "limit": filters.limit,
        "total": total,
        "data": results
    }



# Delete profile
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

    

