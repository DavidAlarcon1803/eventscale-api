from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

# Configuración SSL para Neon
connect_args = {}
if "neon.tech" in DATABASE_URL:
    connect_args = {"ssl": "require"}

# 1. Crear el motor asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args=connect_args,
    # --- AGREGA ESTAS DOS LÍNEAS NUEVAS ---
    pool_pre_ping=True,   # Verifica la conexión antes de usarla (Vital para Neon)
    pool_recycle=300      # Recicla conexiones cada 5 minutos para evitar timeouts
)

# 2. Configurar la fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. Clase Base
class Base(DeclarativeBase):
    pass

# 4. Dependencia
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()