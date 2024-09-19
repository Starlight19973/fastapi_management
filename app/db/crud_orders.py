from sqlalchemy.orm import Session
from . import models, schemas

# Операции для Order (заказа)


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()


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


def update_order_status(db: Session, order_id: int, status: schemas.OrderStatusEnum):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order