from fastapi import APIRouter, Depends, HTTPException
from Infraestructure.database import DB
from dependencies import get_db
from pydantic import BaseModel
import Services.authService as authService

authRouter = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class OAuthLoginRequest(BaseModel):
    provider: str
    oauth_token: str

@authRouter.post("/auth/login", tags=["Auth"])
async def login(request: LoginRequest, db: DB = Depends(get_db)):
    try:
        tokens = await authService.login_with_password(db, request.username, request.password)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Autenticación fallida: {str(e)}")

@authRouter.post("/auth/oauth", tags=["Auth"])
async def oauth_login(request: OAuthLoginRequest, db: DB = Depends(get_db)):
    try:
        tokens = await authService.login_with_oauth(db, request.provider, request.oauth_token)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"OAuth fallido: {str(e)}")



@authRouter.post("/auth/refresh", tags=["Auth"])
async def refresh_token(refresh_token: str, db: DB = Depends(get_db)):
    try:
        tokens = await authService.refresh_access_token(db, refresh_token)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al refrescar token: {str(e)}")
