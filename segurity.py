# from fastapi import HTTPException, Request, Depends
# from fastapi.security import HTTPBearer
# from Infraestructure.database import DB
# from Repositories.tokenRepository import TokenRepository
# from datetime import datetime
# import jwt

# # Configuración del JWT
# SECRET_KEY = "mysecretkey"  # Cambia esto por una clave segura
# ALGORITHM = "HS256"

# # Middleware para autenticar usuarios
# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super().__init__(auto_error=auto_error)

#     async def __call__(self, request: Request, db: DB = Depends()):
#         # Extraer el token del encabezado Authorization: Bearer <token>
#         credentials = await super().__call__(request)
#         if credentials:
#             token = credentials.credentials
#             if not await self.verify_token(token, db):
#                 raise HTTPException(status_code=403, detail="Token inválido o sesión no activa")
#             return token
#         else:
#             raise HTTPException(status_code=403, detail="No se proporcionó un token")



#     async def verify_token(self, token: str, db: DB):
#         try:
#             # Limpieza del token
#             if token.startswith("Bearer "):
#                 token = token.split("Bearer ")[1]  # Elimina el prefijo "Bearer "
#             token = token.strip()  # Elimina espacios en blanco al inicio y al final
#             print("Token después de limpiar:", token)
#             d = ">" + token + "<"
#             print("d: ", d)
            
#             tokenk = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTczNzE0Njg5NX0.u4cQQsI3cSnpGWAgwOp0HJpxmqWtQLaRN3HzIL_krNw"
#             print("Decodificando el tokenk...")
#             payload = jwt.decode(tokenk, SECRET_KEY, algorithms=[ALGORITHM])
#             print(f"Payload decodificado: {payload}")

#             # Consultar el token en la base de datos
#             print("Consultando el token en la base de datos...")
#             token_data = await TokenRepository.get_by_access_token(db, token)

#             if not token_data:
#                 print("Token no encontrado en la base de datos.")
#                 return False

#             print(f"Datos del token en la base de datos: {token_data}")

#             # Verificar estado
#             if token_data["status"] != "active":
#                 print("El token no está activo.")
#                 return False

#             # Verificar expiración
#             if datetime.utcnow() > token_data["expires_at"]:
#                 print("El token ha expirado.")
#                 return False

#             print("El token es válido.")
#             return True
#         except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
#             print(f"Error al decodificar el token: {e}")
#             return False








from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from Infraestructure.database import DB
from Repositories.tokenRepository import TokenRepository
from datetime import datetime
import jwt

# Configuración del JWT
SECRET_KEY = "mysecretkey"  # Asegúrate de que este valor coincida con el de la generación de tokens
ALGORITHM = "HS256"

# Middleware para autenticar usuarios
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: DB = Depends()):
        # Extraer el token del encabezado Authorization: Bearer <token>
        credentials = await super().__call__(request)
        if credentials:
            token = credentials.credentials
            if not await self.verify_token(token, db):
                raise HTTPException(status_code=403, detail="Token inválido o sesión no activa")
            return token
        else:
            raise HTTPException(status_code=403, detail="No se proporcionó un token")

    async def verify_token(self, token: str, db: DB):
        try:
            # Limpieza del token
            if token.startswith("Bearer "):
                token = token.split("Bearer ")[1]  # Elimina el prefijo "Bearer "
            token = token.strip()  # Elimina espacios en blanco al inicio y al final

            print(f"Token después de limpiar: {token}")

            # Decodificar el token dinámico recibido
            print("Decodificando el token...")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"Payload decodificado: {payload}")

            # Consultar el token en la base de datos
            print("Consultando el token en la base de datos...")
            token_data = await TokenRepository.get_by_access_token(db, token)

            if not token_data:
                print("Token no encontrado en la base de datos.")
                return False

            print(f"Datos del token en la base de datos: {token_data}")

            # Verificar estado
            if token_data["status"] != "active":
                print("El token no está activo.")
                return False

            # Verificar expiración
            if datetime.utcnow() > token_data["expires_at"]:
                print("El token ha expirado.")
                return False

            print("El token es válido.")
            return True

        except jwt.ExpiredSignatureError:
            print("El token ha expirado.")
            return False
        except jwt.InvalidTokenError as e:
            print(f"Error al decodificar el token: {e}")
            return False
