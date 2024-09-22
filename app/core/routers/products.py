from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import crud_products
from app.db.database import get_db
from app.db.schemas import Product, ProductCreate

router = APIRouter()


# Создание товара (POST /products)
@router.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud_products.create_product(db=db, product=product)


# Получение списка товаров (GET /products)
@router.get("/products/", response_model=list[Product])
async def get_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud_products.get_products(db, skip=skip, limit=limit)


# Получение информации о товаре по id (GET /products/{id})
@router.get("/products/{id}", response_model=Product)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_products.get_product(db, product_id=id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


# Обновление информации о товаре (PUT /products/{id})
@router.put("/products/{id}", response_model=Product)
async def update_product(id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    existing_product = await crud_products.get_product(db, product_id=id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return await crud_products.update_product(db=db, product_id=id, product=product)


# Удаление товара (DELETE /products/{id})
@router.delete("/products/{id}", response_model=Product)
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await crud_products.get_product(db, product_id=id)
    if product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return await crud_products.delete_product(db=db, product_id=id)


