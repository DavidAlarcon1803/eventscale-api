from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException
from src.models.ticket import Ticket, TicketStatus

async def buy_ticket_service(ticket_id: int, user_id: int, db: AsyncSession):
    """
    Intenta comprar un ticket manejando concurrencia estricta.
    """
    async with db.begin(): # Inicia la transacción
        # 1. SELECT FOR UPDATE
        # Esto bloquea la fila específica en la DB. Si otro proceso intenta
        # hacer un 'for update' en este ID, tendrá que esperar a que soltemos el lock.
        query = select(Ticket).where(Ticket.id == ticket_id).with_for_update()
        result = await db.execute(query)
        ticket = result.scalar_one_or_none()

        # 2. Validaciones
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket no encontrado")
        
        if ticket.status != TicketStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail="El ticket ya no está disponible")

        # 3. Actualizar estado (La compra)
        ticket.status = TicketStatus.SOLD
        ticket.owner_id = user_id
        
        # Al salir del bloque 'async with', se hace commit automáticamente.
        # Si ocurre un error, se hace rollback y se libera el lock.
        
    return ticket