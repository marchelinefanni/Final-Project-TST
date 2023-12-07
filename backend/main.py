from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Request, Form
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from routes.auth import *

from routes.auth import auth_router
from routes.recommendation import recommendation_router
from routes.customization import customization_router
from routes.order import order_router
from routes.product import product_router

app = FastAPI() 
app.include_router(auth_router)
app.include_router(recommendation_router)
app.include_router(customization_router)
app.include_router(order_router)
app.include_router(product_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def welcome():
    return {"message": "Welcome to FashUp! Add /docs to the URL to use the service!"}