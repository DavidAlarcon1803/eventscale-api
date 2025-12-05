from pydantic import BaseModel, EmailStr
from src.models.user import UserRole

# Lo que devolvemos al consultar usuarios
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True

# Lo que recibimos para cambiar el rol
class UserRoleUpdate(BaseModel):
    role: UserRole