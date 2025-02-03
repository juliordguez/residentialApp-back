from Repositories.userRepository import UserRepository
from Repositories.tokenRepository import TokenRepository
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "mysecretkey"  # Cambia esto por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def login_with_password(db, username, password):
    user = await UserRepository.get_by_username(db, username)
    if not user or not pwd_context.verify(password, user["password_hash"]):
        raise Exception("Credenciales inválidas")
    return await generate_tokens(user["id_user"], db)

async def login_with_oauth(db, provider, oauth_token):
    user = await UserRepository.get_by_oauth(db, provider, oauth_token)
    if not user:
        # Si el usuario no existe, regístralo
        user_data = {
            "email": "correo@oauth.com",  # Extrae del token del proveedor
            "id_oauth_provider": provider,
            "id_oauth": oauth_token,
        }
        user = await UserRepository.create(db, user_data)
    return await generate_tokens(user["id_user"], db)



async def generate_tokens(user_id, db):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode({"sub": str(user_id), "exp": datetime.utcnow() + access_token_expires}, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode({"sub": str(user_id), "type": "refresh"}, SECRET_KEY, algorithm=ALGORITHM)

    await TokenRepository.create(db, user_id, access_token, refresh_token, datetime.utcnow() + access_token_expires)
    return {"access_token": access_token, "refresh_token": refresh_token}


async def refresh_access_token(db, refresh_token):
    token_data = await TokenRepository.get_by_refresh_token(db, refresh_token)
    if not token_data or token_data["status"] != "active":
        raise Exception("Token inválido o revocado")

    return await generate_tokens(token_data["id_user"], db)
