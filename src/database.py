from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

# Obtener URL desde variables de entorno (definidas en docker-compose)
# Ejemplo: postgresql+asyncpg://alarcon:password123@db:5432/eventscale
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada")

# 1. Crear el motor asíncrono
# echo=True imprime las consultas SQL en la consola (útil para debug)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 2. Configurar la fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. Clase Base para los modelos
class Base(DeclarativeBase):
    pass

# 4. Dependencia para inyectar la sesión en los endpoints de FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # El commit se hace manualmente en el servicio o automáticamente si usas un manager
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()