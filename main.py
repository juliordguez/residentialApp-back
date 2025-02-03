from fastapi import FastAPI, Depends
from Infraestructure.database import DB
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Especifica el frontend, puede ser "localhost" o un dominio.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = DB()  # Instanciar el objeto DB
    await db.start_pool()  # Iniciar el pool de conexiones
    app.state.db = db  # Guardar la instancia en el estado de la app
    yield
    await db.close_pool()  # Cerrar el pool de conexiones

app.router.lifespan_context = lifespan


from dependencies import get_db
from Routers import roleRouter
from Routers import userRouter
from Routers import authRouter
from Routers import sessionRouter

# Montar los routers e inyectar la instancia de DB
app.include_router(roleRouter.roleRouter)
app.include_router(userRouter.userRouter)
app.include_router(authRouter.authRouter)
app.include_router(sessionRouter.sessionRouter)