from pydantic import BaseModel

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
