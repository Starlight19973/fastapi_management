from fastapi import FastAPI
from app.core.routers import products, orders

app = FastAPI()


app.include_router(products.router)
app.include_router(orders.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.core.main:app", host="127.0.0.1", port=8000, reload=True)