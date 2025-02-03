from Repositories.userRepository import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db, request):
    if request.password:  # Creación con contraseña
        hashed_password = pwd_context.hash(request.password)
        user_data = {
            "username": request.username,
            "email": request.email,
            "password_hash": hashed_password,
        }
    elif request.id_oauth_provider and request.id_oauth:  # Creación con OAuth
        user_data = {
            "email": request.email,
            "id_oauth_provider": request.id_oauth_provider,
            "id_oauth": request.id_oauth,
        }
    else:
        raise Exception("Datos insuficientes para crear un usuario")

    return await UserRepository.create(db, user_data)

async def get_user(db, user_id):
    return await UserRepository.get_by_id(db, user_id)


async def get_all_users(db):
    """
    Obtiene todos los usuarios del repositorio.
    """
    try:
        return await UserRepository.get_all(db)
    except Exception as e:
        print("Excepción en get_all_users:", e)
        raise
