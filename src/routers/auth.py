from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from src.database import get_db
from src.models.user import User
from src.security import (
    verify_password, 
    create_access_token, 
    create_refresh_token, 
    get_password_hash,
    verify_refresh_token
)
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(new_user)
    await db.commit()
    return {"msg": "Usuario creado exitosamente"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Buscar usuario
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar ambos tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }

# 3. REFRESH TOKEN (Nuevo Endpoint)
@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    request: RefreshTokenRequest, 
    db: AsyncSession = Depends(get_db)
):
    # Validar el token de refresh
    email = verify_refresh_token(request.refresh_token)
    
    # Verificar que el usuario siga existiendo y activo
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Usuario inactivo o no encontrado")

    # Rotación de tokens: Emitimos un nuevo Access y (opcionalmente) un nuevo Refresh
    new_access_token = create_access_token(data={"sub": user.email})
    # Opcional: Podrías rotar el refresh token aquí también por seguridad extra
    
    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token, # Devolvemos el mismo o uno nuevo
        "token_type": "bearer"
    }

# 4. LOGOUT (Cierre de Sesión)
@router.post("/logout")
async def logout():
    return {"msg": "Sesión cerrada exitosamente. Elimina los tokens de tu almacenamiento local."}
