from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Literal, Optional


class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50, example="João Silva")
    data_nascimento: datetime = Field(..., example="2010-05-15")
    tipo_usuario: Literal["root", "admin", "aluno", "beneficiario"] = Field(
        ..., example="aluno"
    )
    telefone: str = Field(..., min_length=8, max_length=20, example="51999998888")
    email: Optional[EmailStr] = Field(..., example="email@teste.com")
    senha: str = Field(..., min_length=1, max_length=255, example="senha123")
    cep: str = Field(..., min_length=8, max_length=10, example="90000000")
    logradouro: str = Field(..., min_length=3, max_length=100, example="Rua Teste")
    numero: str = Field(..., min_length=1, max_length=10, example="123")
    bairro: str = Field(..., min_length=3, max_length=50, example="Bairro Teste")
    cidade: str = Field(..., min_length=3, max_length=50, example="Cidade Teste")
    estado: str = Field(..., min_length=2, max_length=50, example="Estado Teste")

    @field_validator("email", mode="before")
    @classmethod
    def tratar_email_vazio(cls, v):
        # Se o usuário digitou uma string vazia "" ou cheia de espaços, transforma em None
        if isinstance(v, str) and v.strip() == "":
            return None
        return v

    @field_validator("tipo_usuario", mode="before")
    @classmethod
    def normalizar_tipo_usuario(cls, v):
        if isinstance(v, str):
            return v.strip().lower().replace("á", "a")
        return v


class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    data_nascimento: datetime
    tipo_usuario: str
    telefone: str
    email: Optional[EmailStr]
    cep: str
    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str

    class Config:
        from_attributes = True


class AlunoCursoResponse(BaseModel):
    id_usuario: int
    nome: str
    idade: int
    cidade: str
    curso: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str
