from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import models, schemas


# Операции для Product (товара)
async def get_product(db: AsyncSession, product_id: int):
    # Используем ORM-запрос через select
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    # ORM-запрос для получения всех продуктов с пропуском и лимитом
    result = await db.execute(
        select(models.Product).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductCreate):
    # Получение продукта по ID через ORM-запрос
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    if db_product:
        # Обновление атрибутов продукта
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.stock_quantity = product.stock_quantity
        await db.commit()
        await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    # Получение продукта по ID через ORM-запрос
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    db_product = result.scalar_one_or_none()
    if db_product:
        # Удаление продукта через ORM-запрос
        await db.delete(db_product)
        await db.commit()
    return db_product
