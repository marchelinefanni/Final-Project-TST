from fastapi import APIRouter, Depends, HTTPException, status 
import json
from routes.auth import *
from models.order import *

order_router = APIRouter(tags=['Orders'])
order = {}

# ORDER MODELS


# READ JSON FILES
# orders.json 
with open("data/orders.json","r") as read_file1:
    orders = json.load(read_file1)

# materials.json 
with open("data/materials.json","r") as read_file2:
    materials = json.load(read_file2)

# catalogue.json 
with open("data/catalogue.json","r") as read_file3:
    catalogue = json.load(read_file3)


# API ENDPOINTS
# MATERIALS AND CATALOGUE
@order_router.get('/materials')
async def read_all_materials(current_user: User = Depends(get_current_active_user)):
    return materials['materials']

@order_router.get('/catalogue')
async def read_all_catalogue(current_user: User = Depends(get_current_active_user)):
    return catalogue['catalogue']


# ORDERS
# CREATE / POST
@order_router.post('/orders')
async def create_order(order: Order, current_user: User = Depends(get_current_active_user)):
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
@order_router.get('/orders')
async def read_all_orders(current_user: User = Depends(get_current_active_user)):
    return orders['orders']

@order_router.get('/orders/{order_id}')
async def read_order(order_id: int, current_user: User = Depends(get_current_active_user)):
    for order in orders['orders']:
        print(order)
        if order['order_id'] == order_id:
            return order 
    raise HTTPException(
        status_code=404, detail=f'ORDER NOT FOUND'
    )

# UPDATE / PUT
@order_router.put('/orders')
async def update_order(order: Order, current_user: User = Depends(get_current_active_user)):
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
@order_router.delete('/orders/{order_id}')
async def delete_order(order_id: int, current_user: User = Depends(get_current_active_user)):
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



# INPUT VALIDATIONS
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
