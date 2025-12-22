from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqEnum
from sqlalchemy.sql import func
from src.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # --- NUEVOS CAMPOS DE PERFIL ---
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    
    # --- ESTADO Y SEGURIDAD ---
    is_active = Column(Boolean, default=True)
    role = Column(SqEnum(UserRole), default=UserRole.USER)
    
    # --- AUDITORÍA (Timestamps) ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
