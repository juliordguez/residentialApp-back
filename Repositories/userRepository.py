class UserRepository:
    @staticmethod
    async def create(db, user_data):
        if "password_hash" in user_data:  # Usuario con contraseña
            query = """
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s)
            """
            params = (user_data["username"], user_data["email"], user_data["password_hash"])
        else:  # Usuario federado
            query = """
            INSERT INTO users (email, id_oauth_provider, id_oauth) 
            VALUES (%s, %s, %s)
            """
            params = (user_data["email"], user_data["id_oauth_provider"], user_data["id_oauth"])
        
        return await db.run_query(query, params)

    @staticmethod
    async def get_by_id(db, user_id):
        query = "SELECT * FROM users WHERE id_user = %s"
        result = await db.run_query(query, (user_id,))
        return result[0] if result else None

    @staticmethod
    async def get_by_username(db, username):
        query = "SELECT * FROM users WHERE username = %s"
        result = await db.run_query(query, (username,))
        return result[0] if result else None

    @staticmethod
    async def get_by_oauth(db, provider, oauth_token):
        query = "SELECT * FROM users WHERE id_oauth_provider = %s AND id_oauth = %s"
        result = await db.run_query(query, (provider, oauth_token))
        return result[0] if result else None



    @staticmethod
    async def get_all(db):
        """
        Obtiene todos los usuarios de la tabla 'users'.
        """
        query = """
        SELECT id_user, username, email, id_rol, id_oauth_provider, id_oauth
        FROM users
        """
        try:
            return await db.run_query(query)
        except Exception as e:
            print("Error en get_all (usuarios):", e)
            raise