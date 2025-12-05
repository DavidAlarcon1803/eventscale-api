from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.event import EventCreate
from src.services.event_service import create_event_with_tickets
# Importamos la dependencia estricta
from src.security import get_current_admin 
from src.models.user import User

router = APIRouter()

# Cambiamos 'get_current_user' por 'get_current_admin'
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin) # <--- Ahora solo entra Admin
):
    # Ya no necesitamos el if current_user.is_superuser... la dependencia lo hizo.
    event = await create_event_with_tickets(event_in, db)
    return {
        "msg": "Evento creado por Administrador",
        "id": event.id,
        "total_tickets": event_in.total_tickets
    }