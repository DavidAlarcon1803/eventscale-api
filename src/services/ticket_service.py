from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from src.models.ticket import Ticket, TicketStatus

async def buy_ticket_service(ticket_id: int, user_id: int, db: AsyncSession):
    """
    Intenta comprar un ticket manejando concurrencia estricta.
    """
    # ELIMINADO: async with db.begin():  <-- Esto causaba el error de doble transacción
    
    # 1. SELECT FOR UPDATE
    # Usamos la transacción que ya viene abierta desde la autenticación (security.py)
    query = select(Ticket).where(Ticket.id == ticket_id).with_for_update()
    result = await db.execute(query)
    ticket = result.scalar_one_or_none()

    # 2. Validaciones
    if not ticket:
        # Importante: Si fallamos, no hacemos commit (el rollback ocurre automático al salir)
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    
    if ticket.status != TicketStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="El ticket ya no está disponible")

    # 3. Actualizar estado (La compra)
    ticket.status = TicketStatus.SOLD
    ticket.owner_id = user_id
    
    # 4. CONFIRMAR LA TRANSACCIÓN
    # Como quitamos el bloque 'async with', debemos guardar explícitamente.
    await db.commit()
    # Refrescamos el objeto para devolver los datos actualizados
    await db.refresh(ticket) 
        
    return ticket