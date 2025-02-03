from Repositories.roleRepository import RoleRepository

async def get_roles(db):
    """
    Obtiene todos los roles.
    """
    try:
        roles = await RoleRepository.get_all(db)
        return roles
    except Exception as e:
        print("Excepción en get_roles:", e)
        raise

async def create_role(db, role_name):
    """
    Crea un nuevo rol.
    """
    try:
        new_role = await RoleRepository.create(db, role_name)
        return new_role
    except Exception as e:
        print("Excepción en create_role:", e)
        raise

async def update_role(db, role_id, role_name):
    """
    Actualiza un rol existente.
    """
    try:
        updated_role = await RoleRepository.update(db, role_id, role_name)
        return updated_role
    except Exception as e:
        print("Excepción en update_role:", e)
        raise

async def delete_role(db, role_id):
    """
    Elimina un rol por ID.
    """
    try:
        success = await RoleRepository.delete(db, role_id)
        return success
    except Exception as e:
        print("Excepción en delete_role:", e)
        raise
