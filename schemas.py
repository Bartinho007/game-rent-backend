from pydantic import BaseModel
from typing import Optional
from typing import List

class ItemBase(BaseModel):
    model: str
    params: Optional[str] = None
    available_count: int
    price_per_day: float
    is_available: bool = True

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    
class CartItem(BaseModel):
    id: int
    count: int

class OrderCreate(BaseModel):
    user_id: int
    user_name: str
    phone: str
    email: str
    delivery_address: str
    items: List[CartItem]

class OrderResponse(BaseModel):
    id: int
    status: str    

    class Config:
        from_attributes = True  # для SQLAlchemy 2.x
