from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.crud_products import create_order, get_orders, get_order, update_order_status
from app.db.database import get_db
from app.db.schemas import Order, OrderCreate, OrderStatusEnum

router = APIRouter()

# Создание заказа (POST /orders)
@router.post("/orders/", response_model=Order)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)

# Получение списка заказов (GET /orders)
@router.get("/orders/", response_model=list[Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_orders(db, skip=skip, limit=limit)

# Получение информации о заказе по id (GET /orders/{id})
@router.get("/orders/{id}", response_model=Order)
def read_order(id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id=id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Обновление статуса заказа (PATCH /orders/{id}/status)
@router.patch("/orders/{id}/status", response_model=Order)
def update_order_status(id: int, status: OrderStatusEnum, db: Session = Depends(get_db)):
    existing_order = get_order(db, order_id=id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return update_order_status(db=db, order_id=id, status=status)