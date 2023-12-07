from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
import json
from routes.auth import *

from routes.auth import auth_router
from routes.recommendation import recommendation_router
from routes.customization import customization_router
from routes.order import order_router

app = FastAPI() 
app.include_router(auth_router)
app.include_router(recommendation_router)
app.include_router(customization_router)
app.include_router(order_router)

@app.get("/")
async def welcome():
    return {"message": "Welcome to FashUp! Add /docs to the URL to use the service!"}
