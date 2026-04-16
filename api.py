import httpx
from fastapi import HTTPException
from fastapi.responses import JSONResponse


client = httpx.AsyncClient(timeout=5.0)


def upstream_error(api_name: str):
    raise HTTPException(
        status_code=502,
        detail=f"{api_name} returned an invalid response"
    )


# Request to external APIs
async def make_api_request(*, url, name, api_name):
    try:
        response = await client.get(url, params={"name": name})
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail=f"{api_name} returned an invalid response"
            )

        return response.json()

    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
           detail=f"{api_name} returned an invalid response"
        )



async def get_data(name: str):
    
    genderize_data = await make_api_request(
        url="https://api.genderize.io",
        name=name,
        api_name="Gendarize"
    )
    
    gender = genderize_data.get("gender")
    gender_probability = genderize_data.get("probability")
    count = genderize_data.get("count")


    # edge case
    if gender is None or count == 0:
        upstream_error("Genderize")
    
    agify_data = await make_api_request(
        url="https://api.agify.io",
        name=name,
        api_name="Agify"
    )

    # Extract age from Agify. Classify age_group: 0–12 → child, 13–19 → teenager, 20–59 → adult, 60+ → senior
    
    age = agify_data.get("age")
    if age is None:
        upstream_error("Agify")
    elif 0 <= age <= 12:
        age_group = 'child'
    elif 13 <= age <= 19:
        age_group = 'teenager'
    elif 20 <= age <= 59:
        age_group = 'adult'
    else:
        age_group = 'senior'


    nationalize_data = await make_api_request(
        url="https://api.nationalize.io",
        name=name,
        api_name="Nationalize"
    )

    #Extract country list from Nationalize. Pick the country with the highest probability as country_id
    countries = nationalize_data.get("country", [])
    if not countries:
        upstream_error("Nationalize")
    else:
        top_country = max(countries, key=lambda x: x["probability"])

    responses = {
        "name": name,
        "gender": gender,
        "gender_probability": float(gender_probability),
        "sample_size": count,
        "age": age,
        "age_group": age_group,
        "country_id": top_country["country_id"],
        "country_probability": top_country["probability"],
    }
    return responses