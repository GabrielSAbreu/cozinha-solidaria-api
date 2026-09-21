from pydantic import BaseModel, Field


class CursoCreate(BaseModel):
    nome_curso: str = Field(
        ..., min_length=3, max_length=100, example="Curso de Python"
    )
    carga_horaria: int = Field(..., gt=0, example=40)


class CursoResponse(BaseModel):
    id_curso: int
    nome_curso: str
    carga_horaria: int

    class Config:
        from_attributes = True
