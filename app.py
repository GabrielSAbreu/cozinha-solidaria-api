from fastapi import FastAPI
from model import db
from fastapi.middleware.cors import CORSMiddleware
from routes import beneficio_router, curso_router, usuario_router

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuario_router)
app.include_router(curso_router)
app.include_router(beneficio_router)
