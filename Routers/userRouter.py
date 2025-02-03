from fastapi import APIRouter, Depends, HTTPException
from Infraestructure.database import DB
from dependencies import get_db
from pydantic import BaseModel, EmailStr
import Services.userService as userService
from segurity import JWTBearer


userRouter = APIRouter(dependencies=[Depends(JWTBearer())]  # Protección para todos los endpoints
)

class UserCreateRequest(BaseModel):
    username: str = None  # Opcional para federación
    email: EmailStr
    password: str = None  # Contraseña para autenticación local
    id_oauth_provider: str = None  # Proveedor OAuth
    id_oauth: str = None  # ID único del usuario en el proveedor

class UserUpdateRequest(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None

@userRouter.post("/users", tags=["Users"])
async def create_user(request: UserCreateRequest, db: DB = Depends(get_db)):
    try:
        user = await userService.create_user(db, request)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@userRouter.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: int, db: DB = Depends(get_db)):
    try:
        user = await userService.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")


@userRouter.get("/users", tags=["Users"])
async def get_all_users(db: DB = Depends(get_db)):
    """
    Obtiene todos los usuarios del sistema.
    """
    try:
        users = await userService.get_all_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los usuarios: {str(e)}")
