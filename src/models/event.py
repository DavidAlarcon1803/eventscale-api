from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    
    # Relación: Un evento tiene muchos tickets
    # (Asegúrate de que el string "Ticket" coincida con el nombre de la clase en ticket.py)
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")
    