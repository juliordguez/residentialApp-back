class TokenRepository:
    @staticmethod
    async def create(db, user_id, access_token, refresh_token, expires_at):
        query = """
        INSERT INTO oauth_token (id_user, access_token, refresh_token, expires_at)
        VALUES (%s, %s, %s, %s)
        """
        return await db.run_query(query, (user_id, access_token, refresh_token, expires_at))



    @staticmethod
    async def get_active_sessions(db, user_id):
        """
        Obtiene todas las sesiones activas de un usuario.
        """
        query = """
        SELECT access_token, refresh_token, expires_at, status 
        FROM oauth_token
        WHERE id_user = %s AND status = 'active'
        """
        return await db.run_query(query, (user_id,))

    @staticmethod
    async def revoke_all(db, user_id):
        """
        Revoca todas las sesiones activas de un usuario.
        """
        query = """
        UPDATE oauth_token
        SET status = 'revoked'
        WHERE id_user = %s AND status = 'active'
        """
        result = await db.run_query(query, (user_id,))
        return result  # Número de sesiones revocadas

    @staticmethod
    async def revoke_token(db, token):
        """
        Revoca un token específico.
        """
        query = """
        UPDATE oauth_token
        SET status = 'revoked'
        WHERE access_token = %s AND status = 'active'
        """
        result = await db.run_query(query, (token,))
        return result > 0  # Devuelve True si se revocó el token
    
            
    @staticmethod
    async def get_by_refresh_token(db, refresh_token):
        query = """
        SELECT id_user, status 
        FROM oauth_token
        WHERE refresh_token = %s
        """
        result = await db.run_query(query, (refresh_token,))
        return result[0] if result else None
    
    @staticmethod
    async def get_by_access_token(db, access_token):
        """
        Obtiene el token por su valor y verifica su estado.
        """
        query = """
        SELECT id_user, status, expires_at
        FROM oauth_token
        WHERE access_token = %s
        """
        result = await db.run_query(query, (access_token,))
        return result[0] if result else None
