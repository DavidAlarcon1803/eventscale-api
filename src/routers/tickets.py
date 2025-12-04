from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.services.ticket_service import buy_ticket_service
from src.security import get_current_user
# Asumiendo que tienes una función helper para publicar en RabbitMQ
from src.rabbitmq_client import publish_message 

router = APIRouter()

@router.post("/buy/{ticket_id}")
async def buy_ticket(
    ticket_id: int, 
    background_tasks: BackgroundTasks, # FastAPI Background Tasks
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user) # Tu dependencia de auth
):
    # 1. Ejecutar la lógica de negocio (Transacción DB)
    sold_ticket = await buy_ticket_service(ticket_id, current_user.id, db)
    
    # 2. Si llegamos aquí, el ticket es nuestro.
    # Ahora delegamos el envío de correo al Worker.
    message_body = {
        "email": current_user.email,
        "ticket_id": sold_ticket.id,
        "event": sold_ticket.event_name,
        "type": "EMAIL_CONFIRMATION"
    }
    
    # Usamos BackgroundTasks para no bloquear la respuesta HTTP mientras conectamos a Rabbit
    background_tasks.add_task(publish_message, "eventscale_queue", message_body)

    return {"status": "success", "ticket": sold_ticket.id}