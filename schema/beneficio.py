from datetime import date

from pydantic import BaseModel, Field


class BeneficioCreate(BaseModel):
    nome_beneficio: str = Field(..., min_length=3, max_length=100)
    descricao: str = Field(..., min_length=3, max_length=255)
    data_entrega: date


class BeneficioResponse(BeneficioCreate):
    id_beneficio: int

    class Config:
        from_attributes = True


class BeneficioUsuarioResponse(BaseModel):
    id_beneficio: int
    nome_beneficio: str
    descricao: str
    data_entrega: date
    status: str
