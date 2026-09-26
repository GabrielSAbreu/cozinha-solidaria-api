from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CursoCreate(BaseModel):
    nome_curso: str = Field(
        ..., min_length=3, max_length=100, example="Curso de Python"
    )
    carga_horaria: int = Field(..., gt=0, example=40)
    data_inicio: date = Field(..., example="2023-01-01")


class CursoResponse(BaseModel):
    id_curso: int
    nome_curso: str
    carga_horaria: int
    data_inicio: Optional[date]

    class Config:
        from_attributes = True
