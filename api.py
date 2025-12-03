from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from db import Item, Order, get_session
from schemas import ItemResponse, ItemCreate, OrderCreate, OrderResponse

app = FastAPI(title="Game Rent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://game-rent-miniapp.vercel.app"],  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    with get_session() as session:
        yield session

@app.get("/items", response_model=List[ItemResponse])
def list_items(
    model: Optional[str] = Query(None),
    only_available: bool = True,
    db: Session = Depends(get_db),
):
    query = db.query(Item)
    if model:
        query = query.filter(Item.model.ilike(f"%{model}%"))
    if only_available:
        query = query.filter(Item.is_available == True, Item.available_count > 0)
    return query.all()

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(
        model=item.model,
        params=item.params,
        available_count=item.available_count,
        price_per_day=item.price_per_day,
        is_available=item.is_available,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # примитивный расчёт общей стоимости
    total_price = 0.0
    items_json = []

    for cart_item in order.items:
        item = db.query(Item).get(cart_item.id)
        if not item or not item.is_available or item.available_count < cart_item.count:
            raise HTTPException(status_code=400, detail=f"Товара id={cart_item.id} нет в нужном количестве")
        total_price += item.price_per_day * cart_item.count
        item.available_count -= cart_item.count
        items_json.append({"id": cart_item.id, "count": cart_item.count})

    from json import dumps
    db_order = Order(
        user_id=order.user_id,
        user_name=order.user_name,
        phone=order.phone,
        email=order.email,
        delivery_address=order.delivery_address,
        items=dumps(items_json, ensure_ascii=False),
        total_price=total_price,
        status="new",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

