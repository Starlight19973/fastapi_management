from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import crud_orders
from app.db.database import get_db
from app.db.schemas import Order, OrderCreate, OrderStatusEnum

router = APIRouter()


# Создание заказа (POST /orders)
@router.post("/orders/", response_model=Order)  # Уберите поле order_items
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud_orders.create_order(db=db, order=order)


# Получение списка заказов (GET /orders)
@router.get("/orders/", response_model=list[Order])
async def get_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud_orders.get_orders(db=db, skip=skip, limit=limit)


# Получение заказа по id (GET /orders/{id})
@router.get("/orders/{id}", response_model=Order)
async def get_order(id: int, db: AsyncSession = Depends(get_db)):
    order = await crud_orders.get_order(db=db, order_id=id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Обновление статуса заказа (PATCH /orders/{id}/status)
@router.patch("/orders/{id}/status", response_model=Order)
async def update_order_status(id: int, status: OrderStatusEnum, db: AsyncSession = Depends(get_db)):
    existing_order = await crud_orders.get_order(db=db, order_id=id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return await crud_orders.update_order_status(db=db, order_id=id, status=status)
