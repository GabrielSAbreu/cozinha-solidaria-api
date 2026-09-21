from fastapi import FastAPI
from model import db
from routes import beneficio_router, curso_router, usuario_router

app = FastAPI()


app.include_router(usuario_router)
app.include_router(curso_router)
app.include_router(beneficio_router)
