from fastapi import APIRouter, Depends, HTTPException
from Infraestructure.database import DB
from dependencies import get_db
import Services.sessionService as sessionService

sessionRouter = APIRouter()

@sessionRouter.get("/sessions/{user_id}", tags=["Sessions"])
async def get_sessions(user_id: int, db: DB = Depends(get_db)):
    """
    Obtiene todas las sesiones activas de un usuario.
    """
    try:
        sessions = await sessionService.get_sessions(db, user_id)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener sesiones: {str(e)}")

@sessionRouter.post("/sessions/revoke/{user_id}", tags=["Sessions"])
async def revoke_all_sessions(user_id: int, db: DB = Depends(get_db)):
    """
    Revoca todas las sesiones activas de un usuario.
    """
    try:
        result = await sessionService.revoke_all_sessions(db, user_id)
        return {"message": f"Se revocaron {result} sesiones activas"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al revocar sesiones: {str(e)}")

@sessionRouter.post("/sessions/revoke_token", tags=["Sessions"])
async def revoke_token(token: str, db: DB = Depends(get_db)):
    """
    Revoca una sesión específica por token.
    """
    try:
        result = await sessionService.revoke_session(db, token)
        if not result:
            raise HTTPException(status_code=404, detail="Token no encontrado o ya revocado")
        return {"message": "Token revocado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al revocar token: {str(e)}")
