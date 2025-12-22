from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.models.user import UserRole

# Base común
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# Registro
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

# Actualizar perfil propio
class UserUpdateProfile(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# Cambio de contraseña
class UserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

# Actualización Admin
class UserAdminUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Respuesta (Salida)
class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
