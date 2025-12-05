from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.event import EventCreate
from src.services.event_service import create_event_with_tickets
from src.security import get_current_user
from src.models.user import User

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validar que sea superusuario (Admin)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, 
            detail="Se requieren permisos de administrador para crear eventos"
        )

    event = await create_event_with_tickets(event_in, db)
    return {
        "msg": "Evento y tickets creados exitosamente",
        "event_id": event.id,
        "total_tickets": event_in.total_tickets
    }
    