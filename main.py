from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel
import json

class Order(BaseModel):
    order_id: int
    material: str 
    weight: int 
    expected_product: str 
    product_quantity: int 

class Material(BaseModel):
    material_id: int 
    material_name: str 

class Catalogue(BaseModel):
    product_id: int 
    product_name: str 
    complexity: int 


# READ JSON FILES
# orders.json 
with open("orders.json","r") as read_file1:
    orders = json.load(read_file1)

# materials.json 
with open("materials.json","r") as read_file2:
    materials = json.load(read_file2)

# catalogue.json 
with open("catalogue.json","r") as read_file3:
    catalogue = json.load(read_file3)

app = FastAPI() 

@app.get("/")
async def welcome():
    return {"message": "Welcome to FashUp! Add /docs to the URL to use the service!"}

# CREATE / POST
@app.post('/orders')
async def create_order(order: Order):
    order_dict = order.dict()
    validate_order(order_dict)
    order_found = False 
    for o in orders['orders']:
        if o['order_id'] == order_dict['order_id']:
            order_found = True 
            return "Order ID " + str(order_dict['order_id']) + " exists."
    if not order_found:
        orders['orders'].append(order_dict)
        with open("orders.json","w") as write_file1:
            json.dump(orders, write_file1)
        return order_dict 
    raise HTTPException(
        status_code=404, detail=f'ORDER NOT FOUND'
    )


# READ / GET
@app.get('/orders')
async def read_all_orders():
    return orders['orders']

@app.get('/orders/{order_id}')
async def read_order(order_id: int):
    for order in orders['orders']:
        print(order)
        if order['order_id'] == order_id:
            return order 
    raise HTTPException(
        status_code=404, detail=f'ORDER NOT FOUND'
    )

@app.get('/materials')
async def read_all_materials():
    return materials['materials']

@app.get('/catalogue')
async def read_all_catalogue():
    return catalogue['catalogue']


# UPDATE / PUT
@app.put('/orders')
async def update_order(order: Order):
    order_dict = order.dict()
    validate_order(order_dict)
    order_found = False
    for id_order, dict_order in enumerate(orders['orders']):
        if dict_order['order_id'] == order_dict['order_id']:
            order_found = True
            orders['orders'][id_order] = order_dict
            with open("orders.json","w") as write_file3:
                json.dump(orders, write_file3)
            return "updated"
    if not order_found:
        return "ORDER NOT FOUND"
    raise HTTPException(
        status_code=404, detail=f'ORDER NOT FOUND'
    )


# DELETE
@app.delete('/orders/{order_id}')
async def delete_order(order_id: int):
    order_found = False 
    for id_order, order in enumerate(orders['orders']):
        if order['order_id'] == order_id:
            order_found = True 
            orders['orders'].pop(id_order)
            with open("orders.json","w") as write_file5:
                json.dump(orders, write_file5)
            return "updated"
    if not order_found:
        return "ORDER NOT FOUND"
    raise HTTPException(
        status_code=404, detail=f'ORDER NOT FOUND'
    )


# CORE FUNCTIONS
# Product Recommendation Based on Material
@app.get('/recommendation')
async def product_recommendation(material_input: str):
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
@app.get('/quantity')
async def quantity_calculator(material_input: str, weight_input: int):
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


# ADDITIONAL FUNCTIONS
def validate_materials(material_input):
    name_found = False
    for material in materials['materials']:
        if material['material_name'] == material_input:
            name_found = True
    if not name_found:
        raise HTTPException(
            status_code=422, detail=f"MATERIAL NOT FOUND"
        )

def validate_catalogue(expected_product):
    name_found = False
    for c in catalogue['catalogue']:
        if c['product_name'] == expected_product:
            name_found = True
    if not name_found:
        raise HTTPException(
            status_code=422, detail=f"PRODUCT NOT FOUND"
        )

def validate_integer(number, name):
    if number < 1:
        raise HTTPException(
            status_code=422, detail=f"{name} SHOULD BE POSITIVE INTEGERS"
        )

def validate_order(order_dict):
    validate_materials(order_dict['material'])
    validate_catalogue(order_dict['expected_product'])
    validate_integer(order_dict['weight'], "WEIGHT")
    validate_integer(order_dict['product_quantity'], "QUANTITY")