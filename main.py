import os
import json
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status, Header, APIRouter, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from database import SessionLocal, create_tables
from models import User

# Cargar variables de entorno del archivo .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Iniciar app con la versión en el título
app = FastAPI(title="API de Gestión de Usuarios", version="1.0.0")
api_router = APIRouter(prefix="/api/v1")

# Esquema Pydantic
class UserCreate(BaseModel):
    user_name: str = Field(..., title="Nombre de usuario")
    user_id: int = Field(..., title="ID de usuario")
    user_email: str = Field(..., title="Correo electrónico del usuario")
    age: Optional[int] = Field(None, title="Edad")
    recommendations: List[str] = Field([], title="Lista de recomendaciones")
    ZIP: Optional[str] = Field(None, title="Código postal")

class UserUpdate(BaseModel):
    user_name: Optional[str] = Field(None, title="Nombre de usuario")
    user_email: Optional[str] = Field(None, title="Correo electrónico del usuario")
    age: Optional[int] = Field(None, title="Edad")
    recommendations: Optional[List[str]] = Field(None, title="Lista de recomendaciones")
    ZIP: Optional[str] = Field(None, title="Código postal")

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    age: Optional[int]
    recommendations: List[str]
    ZIP: Optional[str]

    class Config:
        # Permite la conversión de modelos SQLAlchemy a Pydantic
        from_attributes = True

# Dependencia para la autenticación con API Key
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@api_router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def create_user(user_data: UserCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Crea un nuevo usuario en la base de datos.
    """
    db_user = User(
        user_name=user_data.user_name,
        user_id=user_data.user_id,
        user_email=user_data.user_email,
        age=user_data.age,
        ZIP=user_data.ZIP
    )
    # Asigna la lista de recomendaciones usando el setter de la propiedad
    db_user.recommendations_list = user_data.recommendations

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # Retorna el usuario convertido a UserResponse
        return UserResponse(
            user_id=db_user.user_id,
            user_name=db_user.user_name,
            user_email=db_user.user_email,
            age=db_user.age,
            recommendations=db_user.recommendations_list,
            ZIP=db_user.ZIP
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado."
        )

@api_router.get("/users/{user_id}", response_model=UserResponse, tags=["Usuarios"])
def get_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Obtiene los detalles de un usuario por su ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return UserResponse(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        age=user.age,
        recommendations=user.recommendations_list,
        ZIP=user.ZIP
    )

@api_router.put("/users/{user_id}", response_model=UserResponse, tags=["Usuarios"])
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Actualiza un usuario existente por su ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "recommendations":
            setattr(user, "recommendations_list", value)
        else:
            setattr(user, key, value)
    
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado."
        )
    
    return UserResponse(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        age=user.age,
        recommendations=user.recommendations_list,
        ZIP=user.ZIP
    )

@api_router.delete("/users/{user_id}", status_code=status.HTTP_200_OK, tags=["Usuarios"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    """
    Elimina un usuario por su ID.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": f"Usuario con ID {user_id} eliminado exitosamente."}

# Incluir el router en la aplicación principal
app.include_router(api_router)

# Al iniciar la aplicación, crear las tablas de la base de datos si no existen
@app.on_event("startup")
def on_startup():
    create_tables()
