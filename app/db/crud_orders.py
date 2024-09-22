from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select
from app.db import models, schemas


# Операции для Order (заказа)
async def get_order(db: AsyncSession, order_id: int):
    """Получение заказа по ID с подгрузкой связанных данных"""
    result = await db.execute(
        select(models.Order).options(joinedload(models.Order.order_items)).filter(models.Order.id == order_id)
    )
    return result.scalar_one_or_none()


async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    """Получение списка заказов с подгрузкой связанных данных"""
    result = await db.execute(
        select(models.Order).options(joinedload(models.Order.order_items)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    """Создание нового заказа с проверкой наличия достаточного количества товаров на складе"""
    # Создание нового заказа
    db_order = models.Order(status=order.status)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    # Проверка наличия достаточного количества товаров и обновление их количества
    for item in order.order_items:
        # Получаем продукт по id
        result = await db.execute(select(models.Product).filter(models.Product.id == item.product_id))
        db_product = result.scalar_one_or_none()

        # Проверяем наличие достаточного количества товара на складе
        if db_product is None:
            raise HTTPException(status_code=404, detail=f"Товар с id {item.product_id} не найден!")

        if db_product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара на складе {db_product.name}. Доступно: {db_product.stock_quantity}, Запрошено: {item.quantity}"
            )

        # Уменьшаем количество товара на складе
        db_product.stock_quantity -= item.quantity
        db.add(db_product)

        # Добавляем элемент заказа
        db_order_item = models.OrderItem(order_id=db_order.id, product_id=db_product.id, quantity=item.quantity)
        db.add(db_order_item)

    # Сохраняем изменения
    await db.commit()
    return db_order


async def update_order_status(db: AsyncSession, order_id: int, status: schemas.OrderStatusEnum):
    """Обновление статуса заказа (асинхронно)"""
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    db_order = result.scalar_one_or_none()

    if db_order:
        db_order.status = status
        await db.commit()
        await db.refresh(db_order)
    return db_order