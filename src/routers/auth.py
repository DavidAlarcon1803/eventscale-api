from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate # Importamos del schema centralizado
from src.security import (
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    get_password_hash,
    verify_refresh_token,
    get_token_hash,
    get_current_user
)

router = APIRouter()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Validar existencia
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear usuario
    new_user = User(
        email=user_in.email, 
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        phone_number=user_in.phone_number
    )
    db.add(new_user)
    await db.commit()
    return {"msg": "Usuario creado exitosamente"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    user.active_token_hash = get_token_hash(access_token)
    await db.commit()
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    email = verify_refresh_token(request.refresh_token)
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario no disponible")

    new_access_token = create_access_token(data={"sub": user.email})
    
    user.active_token_hash = get_token_hash(new_access_token)
    await db.commit()
    
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token, 
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Invalida la sesión actual en el servidor."""
    current_user.active_token_hash = None
    await db.commit()
    return {"msg": "Sesión cerrada. Token invalidado."}
