# main.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Imagina que aquí agregarás más rutas y lógica para conectarte a MongoDB.