from datetime import datetime, timedelta
from typing import Optional
import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_db
from src.models.user import User, UserRole

# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================
# En producción, asegúrate de que SECRET_KEY venga de variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Duración larga para el refresh token

# Contexto de seguridad para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de OAuth2 (indica a FastAPI dónde obtener el token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ==========================================
# 🛠️ UTILIDADES DE CONTRASEÑA
# ==========================================
def verify_password(plain_password, hashed_password):
    """Compara una contraseña plana con su hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Genera un hash seguro de la contraseña."""
    return pwd_context.hash(password)


# ==========================================
# 🔑 GENERACIÓN DE TOKENS
# ==========================================
def create_access_token(data: dict):
    """Crea un token de acceso de corta duración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # IMPORTANTE: Marcamos el tipo como 'access'
    to_encode.update({"exp": expire, "type": "access"})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """Crea un token de refresco de larga duración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # IMPORTANTE: Marcamos el tipo como 'refresh'
    to_encode.update({"exp": expire, "type": "refresh"})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================
# 🛡️ VALIDACIÓN Y DEPENDENCIAS
# ==========================================

def verify_refresh_token(token: str):
    """
    Decodifica y valida un Refresh Token.
    Se usa exclusivamente en el endpoint /auth/refresh.
    Devuelve el email (sub) si es válido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido: falta 'sub'")
            
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido: se esperaba tipo 'refresh'")
            
        return email
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh Token expirado o inválido")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    Dependencia principal para proteger rutas.
    Valida el Access Token y recupera el usuario de la BD.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if email is None:
            raise credentials_exception
            
        # SEGURIDAD: Evitar que usen un Refresh Token para acceder a endpoints protegidos
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="El token proporcionado no es un token de acceso"
            )
            
    except JWTError:
        raise credentials_exception
        
    # Buscar usuario en DB
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    # Opcional: Verificar si el usuario está inactivo (baneado)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
        
    return user


async def get_current_admin(current_user: User = Depends(get_current_user)):
    """
    Dependencia para rutas exclusivas de Administradores.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador para realizar esta acción"
        )
    return current_user
