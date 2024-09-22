import enum
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class OrderStatusEnum(enum.Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


# Схема для Product (товара)
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


# Схема для OrderItem (элемент заказа)
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True


# Схема для Order (заказа)
class OrderBase(BaseModel):
    status: OrderStatusEnum = OrderStatusEnum.IN_PROGRESS


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    created_at: datetime
    order_items: List[OrderItem]

    class Config:
        orm_mode = True