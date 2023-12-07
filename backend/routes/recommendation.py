from fastapi import APIRouter, Depends, HTTPException, status 
from routes.auth import *
from routes.order import *

recommendation_router = APIRouter(tags=['Recommendations'])
recommendation = {}

# CORE FUNCTIONS
# Product Recommendation Based on Material
@recommendation_router.get('/recommendation')
async def product_recommendation(material_input: str, current_user: User = Depends(get_current_active_user)):
    validate_materials(material_input)
    recommend = "Here's your product recommendation(s): "
    if material_input == "Denim":
        recommend += "Jacket, Tote bag"
    elif material_input == "Cotton":
        recommend += "Headband, Scarf, Tote bag, Dress, Jacket, Blanket"
    elif material_input == "Wool":
        recommend += "Headband, Scarf, Dress, Jacket"
    elif material_input == "Leather":
        recommend += "Wallet, Tote bag"
    elif material_input == "Silk":
        recommend += "Scarf, Blanket"
    elif material_input == "Linen":
        recommend += "Dress, Tote bag"
    elif material_input == "Polyester":
        recommend += "Headband, Scarf, Tote bag, Dress, Jacket"
    elif material_input == "Flanel":
        recommend += "Headband, Jacket"
    return [recommend]


# Quantity Calculator Based on Material and Weight
@recommendation_router.get('/quantity')
async def quantity_calculator(material_input: str, weight_input: int, current_user: User = Depends(get_current_active_user)):
    validate_materials(material_input)
    validate_integer(weight_input, "WEIGHT")

    # count the material area based on the weight
    if material_input == "Denim":
        area = weight_input / 500
    elif material_input == "Cotton":
        area = weight_input / 250
    elif material_input == "Wool":
        area = weight_input / 400
    elif material_input == "Leather":
        area = weight_input / 5000
    elif material_input == "Silk":
        area = weight_input / 190
    elif material_input == "Linen":
        area = weight_input / 200
    elif material_input == "Polyester":
        area = weight_input / 250
    elif material_input == "Flanel":
        area = weight_input / 300
    
    # count the quantity based on the area
    headband_quantity = area // 0.2
    scarf_quantity = area // 1
    tote_bag_quantity = area // 1
    wallet_quantity = area // 0.1
    blanket_quantity = area // 2
    dress_quantity = area // 2
    jacket_quantity = area // 2

    # create dictionary
    quantity_dict = {
        "headband": headband_quantity,
        "scarf": scarf_quantity,
        "tote_bag": tote_bag_quantity,
        "wallet": wallet_quantity,
        "blanket": blanket_quantity,
        "dress": dress_quantity,
        "jacket": jacket_quantity
    }

    return ["With that amount of material, you can get:", quantity_dict]

