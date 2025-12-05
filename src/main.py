from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import engine, Base
from src.routers import tickets, auth, events # <--- Agrega 'events'
# Importar TODOS los modelos aquí para que Base.metadata los vea
from src.models.user import User
from src.models.ticket import Ticket
from src.models.event import Event # <--- Importante

@asynccontextmanager
async def lifespan(app: FastAPI):
    # NOTA: En producción real se usa Alembic.
    # Como cambiamos la estructura de tablas, esto intentará crearlas.
    # Si da error, tendremos que borrar las tablas viejas en Neon.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="EventScale API", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(events.router, prefix="/events", tags=["Events"]) # <--- Nuevo Router

@app.get("/")
def root():
    return {"message": "EventScale API is running 🚀"}