from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
from urllib.parse import urlsplit


class CursoCreate(BaseModel):
    nome_curso: str = Field(
        ..., min_length=3, max_length=100, example="Curso de Python"
    )
    carga_horaria: int = Field(..., gt=0, example=40)
    data_inicio: date = Field(..., example="2023-01-01")
    imagem_url: Optional[str] = Field(None, max_length=2048)

    @field_validator("imagem_url", mode="before")
    @classmethod
    def validar_imagem_url(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        if not isinstance(value, str):
            return value

        imagem_url = value.strip()
        parsed_url = urlsplit(imagem_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("Informe uma URL de imagem HTTP ou HTTPS válida.")
        return imagem_url


class CursoResponse(BaseModel):
    id_curso: int
    nome_curso: str
    carga_horaria: int
    data_inicio: date
    imagem_url: Optional[str]

    class Config:
        from_attributes = True
