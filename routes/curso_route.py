from fastapi import APIRouter, Depends, Header, HTTPException, status
from typing import List

from model import Session
from model.curso import Curso
from model.cursa import Cursa
from model.usuario import Usuario
from routes.permissions import usuario_com_permissao_admin, usuario_root
from schema.curso import CursoCreate, CursoResponse

router = APIRouter(prefix="/cursos", tags=["Cursos"])


@router.get("/inscricoes/{id_usuario}", response_model=List[int])
def listar_inscricoes(id_usuario: int):
    session = Session()
    try:
        return [
            inscricao.fk_curso_id_curso
            for inscricao in session.query(Cursa)
            .filter(Cursa.fk_usuario_id_usuario == id_usuario)
            .all()
        ]
    finally:
        session.close()


@router.post("/{id_curso}/inscricao", status_code=status.HTTP_201_CREATED)
def inscrever_usuario(
    id_curso: int,
    user_id: int | None = Header(default=None, alias="X-User-Id"),
):
    session = Session()
    try:
        usuario = session.get(Usuario, user_id) if user_id is not None else None
        if usuario is None or usuario.tipo_usuario.lower() != "aluno":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas alunos podem se inscrever nas oficinas.",
            )

        curso = session.get(Curso, id_curso)
        if curso is None:
            raise HTTPException(status_code=404, detail="Curso não encontrado.")

        inscricao = (
            session.query(Cursa)
            .filter(
                Cursa.fk_usuario_id_usuario == usuario.id_usuario,
                Cursa.fk_curso_id_curso == curso.id_curso,
            )
            .first()
        )
        if inscricao is None:
            session.add(
                Cursa(
                    fk_usuario_id_usuario=usuario.id_usuario,
                    fk_curso_id_curso=curso.id_curso,
                    status="inscrito",
                )
            )
            session.commit()

        return {"id_curso": curso.id_curso, "status": "inscrito"}
    except HTTPException:
        raise
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500, detail="Não foi possível registrar a inscrição."
        )
    finally:
        session.close()


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
def excluir_curso(id_curso: int, _usuario=Depends(usuario_com_permissao_admin)):
    session = Session()
    try:
        curso = session.get(Curso, id_curso)
        if curso is None:
            raise HTTPException(status_code=404, detail="Curso não encontrado.")
        session.delete(curso)
        session.commit()
    finally:
        session.close()
