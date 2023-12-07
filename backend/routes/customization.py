from fastapi import APIRouter, Depends, HTTPException, status 
import requests
from routes.auth import *

# Get New Token
def get_new_token():
    payload = {
        "username": "fanni",
        "password": "tst18221090"
    }
    r = requests.post('https://customizedclothintegrated.salmonbeach-997612a6.australiaeast.azurecontainerapps.io/authentications/login', data=payload)
    return r.json()['access_token']

# Request with Token
def authenticate_request(url, payload):
    token = get_new_token()
    # Set Authentication Header
    headers = {'Authoziation': f'Bearer {token}'}
    # Create Request with Header and Body
    r = requests.get(url, headers = headers, data = payload)
    # Token Invalid
    if r.status_code == 401:
        token = get_new_token()
        headers = {'Authorization': f'Bearer {token}'}
        r = requests.get(url, headers=headers, data=payload)
    return r

customization_router = APIRouter(tags=['Customizations'])

customization = {}

# GET CUSTOMIZATION INSPIRATION
@customization_router.get('/customization')
async def customization_inspiration(font: str, color: str, size: str, product_type: str, current_user: User = Depends(get_current_active_user)):
    response = authenticate_request(f'https://customizedclothintegrated.salmonbeach-997612a6.australiaeast.azurecontainerapps.io/customizationRequests/{font}/{color}/{size}/{product_type}', {})
    return response.json()