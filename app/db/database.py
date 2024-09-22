from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.db.db_config import settings


# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

# Создаем фабрику асинхронных сессий
async_session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)


# Функция для получения асинхронной сессии
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# Проверка подключения к базе данных
async def check_db_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT VERSION()"))
        print(f"{result.first()=}")
        await conn.commit()
