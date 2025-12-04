from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base # Asume que ya creaste tu Base en database.py

class TicketStatus(str, enum.Enum):
    AVAILABLE = "available"
    LOCKED = "locked" # Opcional: para un bloqueo lógico temporal
    SOLD = "sold"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index=True) # Simplificado para el ejemplo
    seat_number = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    
    status = Column(Enum(TicketStatus), default=TicketStatus.AVAILABLE)
    
    # Relación con el usuario que lo compró
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())