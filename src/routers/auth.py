from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.user import User
from src.security import verify_password, create_access_token, get_password_hash
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si existe
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(new_user)
    await db.commit()
    return {"msg": "Usuario creado exitosamente"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Buscar usuario
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}