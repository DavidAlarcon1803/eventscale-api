from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserResponse, UserUpdateProfile, UserChangePassword, UserAdminUpdate
from src.security import get_current_user, get_current_admin, get_password_hash, verify_password

router = APIRouter()

# --- ÁREA PERSONAL ---

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_own_profile(
    user_update: UserUpdateProfile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.phone_number is not None:
        current_user.phone_number = user_update.phone_number
    
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/me/change-password")
async def change_password(
    password_data: UserChangePassword,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    if password_data.old_password == password_data.new_password:
        raise HTTPException(status_code=400, detail="La nueva contraseña debe ser diferente")

    current_user.hashed_password = get_password_hash(password_data.new_password)
    await db.commit()
    return {"msg": "Contraseña actualizada exitosamente"}

# --- ÁREA ADMIN ---

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0, 
    limit: int = 20,
    search: str | None = Query(None, min_length=3),
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    query = select(User)
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            or_(User.email.ilike(search_filter), User.full_name.ilike(search_filter))
        )
    query = query.offset(skip).limit(limit).order_by(User.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@router.patch("/{user_id}/admin-update", response_model=UserResponse)
async def admin_update_user(
    user_id: int, 
    update_data: UserAdminUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_edit = result.scalar_one_or_none()
    
    if not user_to_edit:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_to_edit.id == current_admin.id and update_data.role is not None:
        raise HTTPException(status_code=400, detail="No puedes cambiar tu propio rol")

    if update_data.role:
        user_to_edit.role = update_data.role
    if update_data.is_active is not None:
        user_to_edit.is_active = update_data.is_active
        
    await db.commit()
    await db.refresh(user_to_edit)
    return user_to_edit
