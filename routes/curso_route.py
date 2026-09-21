from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from model import Session
from model.curso import Curso
from routes.permissions import usuario_com_permissao_admin, usuario_root
from schema.curso import CursoCreate, CursoResponse

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("", response_model=List[CursoResponse])
def listar_cursos():
    session = Session()
    try:
        return session.query(Curso).all()
    finally:
        session.close()


@router.get("/{id_curso}", response_model=CursoResponse)
def buscar_curso(id_curso: int):
    session = Session()
    try:
        curso = session.get(Curso, id_curso)
        if curso is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado.",
            )
        return curso
    finally:
        session.close()


@router.post("", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def criar_curso(
    curso_dados: CursoCreate, _usuario=Depends(usuario_com_permissao_admin)
):
    session = Session()
    try:
        curso = Curso(**curso_dados.model_dump())
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso
    finally:
        session.close()


@router.put("/{id_curso}", response_model=CursoResponse)
def editar_curso(
    id_curso: int,
    curso_dados: CursoCreate,
    _usuario=Depends(usuario_com_permissao_admin),
):
    session = Session()
    try:
        curso = session.get(Curso, id_curso)
        if curso is None:
            raise HTTPException(status_code=404, detail="Curso não encontrado.")
        for campo, valor in curso_dados.model_dump().items():
            setattr(curso, campo, valor)
        session.commit()
        session.refresh(curso)
        return curso
    finally:
        session.close()


@router.delete("/{id_curso}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_curso(id_curso: int, _usuario=Depends(usuario_root)):
    session = Session()
    try:
        curso = session.get(Curso, id_curso)
        if curso is None:
            raise HTTPException(status_code=404, detail="Curso não encontrado.")
        session.delete(curso)
        session.commit()
    finally:
        session.close()
