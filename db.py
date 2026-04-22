from sqlmodel import create_engine, Session, SQLModel, func, select
import json

from .models import ProfileCreate, Profile




sqlite_filename = 'my_db.db'
sqlite_url = f'sqlite:///./{sqlite_filename}'

engine = create_engine(
    sqlite_url,
    connect_args={'check_same_thread': False},
    echo=True
)


with open('seed_profiles.json') as file:
    data = json.load(file)



def init_db(session: Session) -> None:

    SQLModel.metadata.create_all(engine)

    # Check if table already has data
    count = session.exec(select(func.count()).select_from(Profile)).one()
    if count > 0:
        return
    
    for value in data["profiles"]:
        profile_create = ProfileCreate(
            name = value.get("name"),
            gender = value.get("gender"),
            gender_probability = value.get("gender_probability"),
            age = value.get("age"),
            age_group = value.get("age_group"),
            country_id = value.get("country_id"),
            country_name = value.get("country_name"),
            country_probability = value.get("country_probability")
        )
        profile = Profile.model_validate(profile_create)
        session.add(profile)
    session.commit()

