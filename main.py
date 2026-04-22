from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from .routes import router     
from sqlmodel import Session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, init_db





@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        init_db(session)
        yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail}
    )


app.include_router(router)
