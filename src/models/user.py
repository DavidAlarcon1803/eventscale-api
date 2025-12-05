from sqlalchemy import Column, Integer, String, Boolean, Enum as SqEnum
from src.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"  # Puede gestionar usuarios y eventos
    USER = "user"    # Solo puede comprar tickets

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Campo de Rol: Por defecto todo el mundo nace como 'user'
    role = Column(SqEnum(UserRole), default=UserRole.USER)