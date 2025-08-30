import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

load_dotenv()

# URL підключення до бази даних
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./sqlite3.db")

# Створюємо engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # логування SQL-запитів
)

# Сесії (фабрика)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Базовий клас для моделей
Base = declarative_base()


# Dependency (для FastAPI)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def delete_and_create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Database and tables dropped.")
        await conn.run_sync(Base.metadata.create_all)
        print("Database and tables created.")
