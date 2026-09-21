from fastapi import APIRouter, Depends, HTTPException, status

from model import Session
from model.beneficio import Beneficio
from routes.permissions import usuario_com_permissao_admin, usuario_root
from schema.beneficio import BeneficioCreate, BeneficioResponse

router = APIRouter(prefix="/beneficios", tags=["Benefícios"])


@router.post("", response_model=BeneficioResponse, status_code=status.HTTP_201_CREATED)
def criar_beneficio(
    beneficio_dados: BeneficioCreate,
    _usuario=Depends(usuario_com_permissao_admin),
):
    session = Session()
    try:
        beneficio = Beneficio(**beneficio_dados.model_dump())
        session.add(beneficio)
        session.commit()
        session.refresh(beneficio)
        return beneficio
    finally:
        session.close()


@router.put("/{id_beneficio}", response_model=BeneficioResponse)
def editar_beneficio(
    id_beneficio: int,
    beneficio_dados: BeneficioCreate,
    _usuario=Depends(usuario_com_permissao_admin),
):
    session = Session()
    try:
        beneficio = session.get(Beneficio, id_beneficio)
        if beneficio is None:
            raise HTTPException(status_code=404, detail="Benefício não encontrado.")
        for campo, valor in beneficio_dados.model_dump().items():
            setattr(beneficio, campo, valor)
        session.commit()
        session.refresh(beneficio)
        return beneficio
    finally:
        session.close()


@router.delete("/{id_beneficio}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_beneficio(id_beneficio: int, _usuario=Depends(usuario_root)):
    session = Session()
    try:
        beneficio = session.get(Beneficio, id_beneficio)
        if beneficio is None:
            raise HTTPException(status_code=404, detail="Benefício não encontrado.")
        session.delete(beneficio)
        session.commit()
    finally:
        session.close()
