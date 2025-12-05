from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.ticket import Ticket, TicketStatus
from src.security import get_current_admin # Usamos la nueva dependencia
from src.models.user import User

router = APIRouter()

@router.post("/tickets/{ticket_id}/release")
async def release_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(get_current_admin) # <--- Candado de seguridad
):
    """
    Permite a un administrador cancelar una compra y liberar el asiento.
    """
    # 1. Buscar el ticket
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    # 2. Verificar que esté vendido (no tiene sentido liberar uno disponible)
    if ticket.status != TicketStatus.SOLD:
        raise HTTPException(status_code=400, detail="El ticket no está vendido, no se puede liberar")

    # 3. Lógica de Reversa (Liberación)
    ticket.status = TicketStatus.AVAILABLE
    ticket.owner_id = None # Quitamos al dueño
    
    # Guardamos cambios
    await db.commit()
    await db.refresh(ticket)

    return {
        "msg": f"Ticket {ticket_id} liberado exitosamente por admin {admin_user.email}",
        "status": ticket.status,
        "seat": ticket.seat_number
    }