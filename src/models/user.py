from sqlalchemy import Column, Integer, String, Boolean, Enum as SqEnum
from src.database import Base
import enum

# Definimos los roles posibles
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Nuevo campo de Rol (Por defecto todos son usuarios normales)
    role = Column(SqEnum(UserRole), default=UserRole.USER)