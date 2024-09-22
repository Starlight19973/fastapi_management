import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.core.main import app
from app.db.database import async_session


@pytest.fixture(scope="module")
def test_app():
    yield app


@pytest.fixture(scope="function")
async def test_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_order(test_client):
    # Данные для создания заказа
    order_data = {
        "status": "IN_PROGRESS",
        "order_items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }

    # Выполняем POST-запрос для создания заказа
    response = await test_client.post("/orders/", json=order_data)

    assert response.status_code == 200
    order = response.json()
    assert order["status"] == "IN_PROGRESS"
    assert len(order["order_items"]) == 1
    assert order["order_items"][0]["quantity"] == 2


@pytest.mark.asyncio
async def test_get_orders(test_client):
    # Выполняем GET-запрос для получения списка заказов
    response = await test_client.get("/orders/")

    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)
    if orders:
        assert "status" in orders[0]
        assert "order_items" in orders[0]


@pytest.mark.asyncio
async def test_update_order_status(test_client):
    # Обновим статус заказа с ID = 1
    order_id = 1
    new_status = "SHIPPED"
    response = await test_client.patch(f"/orders/{order_id}/status", json={"status": new_status})

    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == new_status