from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import URL, create_engine, text
from db_config import settings


engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)


with engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(f"{res.first()=}")
    conn.commit()
