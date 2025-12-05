from sqlalchemy.ext.asyncio import AsyncSession
from src.models.event import Event
from src.models.ticket import Ticket, TicketStatus
from src.schemas.event import EventCreate

async def create_event_with_tickets(event_data: EventCreate, db: AsyncSession):
    # 1. Crear el Evento
    new_event = Event(
        name=event_data.name,
        date=event_data.date,
        location=event_data.location
    )
    db.add(new_event)
    await db.flush()  # Esto asigna un ID al evento sin hacer commit final todavía

    # 2. Generar la lista de Tickets en memoria
    # Generamos tickets con asientos "A-1", "A-2", etc.
    tickets_to_create = []
    for i in range(1, event_data.total_tickets + 1):
        ticket = Ticket(
            event_id=new_event.id,
            seat_number=f"Seat-{i}",
            price=event_data.ticket_price,
            status=TicketStatus.AVAILABLE
        )
        tickets_to_create.append(ticket)

    # 3. Inserción Masiva (Batch Insert)
    # add_all es mucho más rápido que hacer un add() por cada ticket
    db.add_all(tickets_to_create)
    
    await db.commit()
    await db.refresh(new_event)
    
    return new_event