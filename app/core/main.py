from fastapi import FastAPI
from core.routers import products, orders

app = FastAPI()

app.include_router(products.router)
app.include_router(orders.router)

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("core.main:app", host="127.0.0.1", port=8000, reload=True)