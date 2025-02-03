class RoleRepository:
    @staticmethod
    async def get_all(db):
        query = "SELECT * FROM roles"
        try:
            roles = await db.run_query(query)
            return roles
        except Exception as e:
            print("Error en get_all (roles):", e)
            raise

    @staticmethod
    async def create(db, role_name):
        query = "INSERT INTO roles (role_name) VALUES (%s)"
        try:
            role_id = await db.run_query(query, (role_name,))
            return {"id": role_id, "role_name": role_name}
        except Exception as e:
            print("Error en create (roles):", e)
            raise

    @staticmethod
    async def update(db, role_id, role_name):
        query = "UPDATE roles SET role_name = %s WHERE id = %s"
        try:
            await db.run_query(query, (role_name, role_id))
            return {"id": role_id, "role_name": role_name}
        except Exception as e:
            print("Error en update (roles):", e)
            raise

    @staticmethod
    async def delete(db, role_id):
        query = "DELETE FROM roles WHERE id = %s"
        try:
            rows_deleted = await db.run_query(query, (role_id,))
            return rows_deleted > 0
        except Exception as e:
            print("Error en delete (roles):", e)
            raise
