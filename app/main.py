# app/main.py

from fastapi import FastAPI
from app.controllers import address_controller, distance_controller
from app.models.base import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(address_controller.router)
app.include_router(distance_controller.router)
