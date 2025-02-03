from Repositories.tokenRepository import TokenRepository

async def get_sessions(db, user_id):
    """
    Obtiene todas las sesiones activas de un usuario.
    """
    try:
        return await TokenRepository.get_active_sessions(db, user_id)
    except Exception as e:
        print("Error en get_sessions:", e)
        raise

async def revoke_all_sessions(db, user_id):
    """
    Revoca todas las sesiones activas de un usuario.
    """
    try:
        return await TokenRepository.revoke_all(db, user_id)
    except Exception as e:
        print("Error en revoke_all_sessions:", e)
        raise

async def revoke_session(db, token):
    """
    Revoca una sesión específica por token.
    """
    try:
        return await TokenRepository.revoke_token(db, token)
    except Exception as e:
        print("Error en revoke_session:", e)
        raise
