from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import engine, Base
from src.routers import tickets, auth

# Función lifespan para tareas al inicio/cierre (como crear tablas en dev)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar (solo para desarrollo, en prod usa Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="EventScale API", lifespan=lifespan)

# Registrar Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# Nota: En tickets.py, asegúrate de importar get_current_user desde src.security
# y ajustar la dependencia en el router
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])

@app.get("/")
def root():
    return {"message": "EventScale API is running 🚀"}