from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.db.schemas import OrderStatusEnum

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)

    # Здесь back_populates связывает таблицы Products и OrderItems
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.IN_PROGRESS)

    # Добавляем lazy='joined' для явной загрузки
    order_items = relationship("OrderItem", back_populates="order", lazy='joined')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    # Связь с Order
    order = relationship("Order", back_populates="order_items", lazy='joined')

    # Связь с Product
    product = relationship("Product", back_populates="order_items", lazy='joined')


