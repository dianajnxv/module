import uvicorn
from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers.users import users_router
from app.routers.records import records_router

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(users_router)
app.include_router(records_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=False)
