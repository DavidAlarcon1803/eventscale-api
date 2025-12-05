from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

class TicketStatus(str, enum.Enum):
    AVAILABLE = "available"
    LOCKED = "locked"
    SOLD = "sold"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- CAMBIO IMPORTANTE: Vinculación con Evento ---
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="tickets")
    # -------------------------------------------------

    seat_number = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.AVAILABLE)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())