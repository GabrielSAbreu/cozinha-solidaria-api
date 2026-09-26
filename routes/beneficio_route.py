from fastapi import APIRouter, Depends, Header, HTTPException, status
from typing import List

from model import Session
from model.beneficio import Beneficio
from model.recebe import Recebe
from model.usuario import Usuario
from routes.permissions import usuario_com_permissao_admin, usuario_root
from schema.beneficio import (
    BeneficioCreate,
    BeneficioResponse,
    BeneficioUsuarioResponse,
)

router = APIRouter(prefix="/beneficios", tags=["Benefícios"])


@router.get("/usuario/{id_usuario}", response_model=List[BeneficioUsuarioResponse])
def listar_beneficios_usuario(
    id_usuario: int,
    user_id: int | None = Header(default=None, alias="X-User-Id"),
):
    if user_id != id_usuario:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    session = Session()
    try:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None or usuario.tipo_usuario.lower() != "beneficiario":
            raise HTTPException(
                status_code=403,
                detail="Apenas beneficiários podem consultar benefícios.",
            )
        recebimentos = {
            recebimento.fk_beneficio_id_beneficio: recebimento.status
            for recebimento in session.query(Recebe)
            .filter(Recebe.fk_usuario_id_usuario == id_usuario)
            .all()
        }
        return [
            {
                "id_beneficio": beneficio.id_beneficio,
                "nome_beneficio": beneficio.nome_beneficio,
                "descricao": beneficio.descricao,
                "data_entrega": beneficio.data_entrega,
                "status": recebimentos.get(beneficio.id_beneficio, "agendado"),
            }
            for beneficio in session.query(Beneficio)
            .order_by(Beneficio.data_entrega)
            .all()
        ]
    finally:
        session.close()


@router.get("", response_model=List[BeneficioResponse])
def listar_beneficios():
    session = Session()
    try:
        return session.query(Beneficio).all()
    finally:
        session.close()


@router.get("/{id_beneficio}", response_model=BeneficioResponse)
def buscar_beneficio(id_beneficio: int):
    session = Session()
    try:
        beneficio = session.get(Beneficio, id_beneficio)
        if beneficio is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Benefício não encontrado.",
            )
        return beneficio
    finally:
        session.close()


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
