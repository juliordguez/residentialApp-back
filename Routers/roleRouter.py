from fastapi import APIRouter, Depends, HTTPException
from Infraestructure.database import DB
from dependencies import get_db
import Services.roleService as roleService
from pydantic import BaseModel

roleRouter = APIRouter()

class RoleCreateRequest(BaseModel):
    role_name: str

class RoleUpdateRequest(BaseModel):
    role_name: str

@roleRouter.get("/roles", tags=["Roles"])
async def get_roles(db: DB = Depends(get_db)):
    try:
        roles = await roleService.get_roles(db)
        return roles
    except Exception as e:
        print("Excepción en get_roles:", e)
        raise HTTPException(status_code=500, detail="Error al obtener los roles")

@roleRouter.post("/roles", tags=["Roles"])
async def create_role(request: RoleCreateRequest, db: DB = Depends(get_db)):
    try:
        new_role = await roleService.create_role(db, request.role_name)
        return new_role
    except Exception as e:
        print("Excepción en create_role:", e)
        raise HTTPException(status_code=500, detail="Error al crear el rol")

@roleRouter.put("/roles/{role_id}", tags=["Roles"])
async def update_role(role_id: int, request: RoleUpdateRequest, db: DB = Depends(get_db)):
    try:
        updated_role = await roleService.update_role(db, role_id, request.role_name)
        return updated_role
    except Exception as e:
        print(f"Excepción en update_role para role_id={role_id}:", e)
        raise HTTPException(status_code=500, detail=f"Error al actualizar el rol con ID {role_id}")

@roleRouter.delete("/roles/{role_id}", tags=["Roles"])
async def delete_role(role_id: int, db: DB = Depends(get_db)):
    try:
        success = await roleService.delete_role(db, role_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"El rol con ID {role_id} no fue encontrado")
        return {"message": f"Rol {role_id} eliminado exitosamente"}
    except Exception as e:
        print(f"Excepción en delete_role para role_id={role_id}:", e)
        raise HTTPException(status_code=500, detail=f"Error al eliminar el rol con ID {role_id}")
