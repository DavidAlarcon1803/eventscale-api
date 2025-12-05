from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from src.database import get_db
from src.models.user import User, UserRole
from src.schemas.user import UserResponse, UserRoleUpdate
from src.security import get_current_admin  # <--- Solo Admins pueden entrar aquí

router = APIRouter()

# 1. LISTAR TODOS LOS USUARIOS (Solo Admin)
@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users

# 2. CAMBIAR EL ROL DE UN USUARIO (Ascender/Degradar)
@router.patch("/{user_id}/role", response_model=UserResponse)
async def change_user_role(
    user_id: int, 
    role_data: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    # Buscar al usuario objetivo
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_edit = result.scalar_one_or_none()
    
    if not user_to_edit:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Evitar que un admin se quite permisos a sí mismo por error (seguridad básica)
    if user_to_edit.id == current_admin.id and role_data.role == UserRole.USER:
        raise HTTPException(status_code=400, detail="No puedes quitarte el rol de admin a ti mismo")

    # Actualizar Rol
    user_to_edit.role = role_data.role
    
    await db.commit()
    await db.refresh(user_to_edit)
    
    return user_to_edit

# 3. DESACTIVAR USUARIO (Banear)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_edit = result.scalar_one_or_none()
    
    if not user_to_edit:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_to_edit.is_active = False # Soft delete (mejor que borrarlo)
    await db.commit()
    return None