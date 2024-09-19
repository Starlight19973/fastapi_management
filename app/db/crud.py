from sqlalchemy.orm import Session
from . import models, schemas


# Операции для Product
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Операции для Order
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Добавляем элементы заказа
    for item in order.order_items:
        db_order_item = models.OrderItem(order_id=db_order.id, **item.dict())
        db.add(db_order_item)

    db.commit()
    return db_order


# Операции для OrderItem
def get_order_items(db: Session, order_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
