from fastapi import Depends
from typing import Annotated
from sqlmodel import Session

from .db import engine



def get_db():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]




