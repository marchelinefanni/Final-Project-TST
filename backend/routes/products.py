from fastapi import APIRouter, Depends, HTTPException, status 
import requests
from routes.auth import *
from routes.customization import *

product_router = APIRouter(tags=['Products'])
product = {}


# GET PRODUCTS
@product_router.get('/products')
async def read_all_products(current_user: User = Depends(get_current_active_user)):
    response = get_request(f'https://customizedclothintegrated.salmonbeach-997612a6.australiaeast.azurecontainerapps.io/products', {})
    return response.json()

@product_router.get('/products/{product_id}')
async def read_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    response = get_request(f'https://customizedclothintegrated.salmonbeach-997612a6.australiaeast.azurecontainerapps.io/products/{product_id}', {})
    return response.json()

@product_router.post('/products')
async def create_product(description: str, price: str, stock: str, default_font: str, default_color: str, size: str, productType: str, imageurl: str,current_user: User = Depends(get_current_active_user)):
    response = post_request(f'https://customizedclothintegrated.salmonbeach-997612a6.australiaeast.azurecontainerapps.io/products?description={description}&price={price}&stock={stock}&default_font={default_font}&default_color={default_color}&size={size}&productType={productType}&imageurl={imageurl}', {})
    return response.json()