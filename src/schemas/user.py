from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from src.models.user import UserRole

# 1. Base común
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# 2. Creación (Registro)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

# 3. Actualización por el propio Usuario (No puede cambiar su rol ni email fácilmente)
class UserUpdateProfile(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# 4. Cambio de Contraseña
class UserChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

# 5. Actualización por Admin (Puede cambiar roles y estado)
class UserAdminUpdate(BaseModel):
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# 6. Respuesta Pública (Output)
class UserResponse(UserBase):
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime  # Importante para debug

    class Config:
        from_attributes = True
