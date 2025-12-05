from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    date: datetime
    location: str
    total_tickets: int  # ¿Cuántas entradas generar? (Ej: 100, 5000)
    ticket_price: int   # Precio por entrada