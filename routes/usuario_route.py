from fastapi import APIRouter, Header, HTTPException, status
from typing import List
from model import Session
from model.usuario import Usuario
from schema import UsuarioCreate, UsuarioLogin, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("", response_model=List[UsuarioResponse])
def listar_usuarios():
    session = Session()
    try:
        return session.query(Usuario).all()
    finally:
        session.close()


@router.get("/{id_usuario}", response_model=UsuarioResponse)
def buscar_usuario(id_usuario: int):
    session = Session()
    try:
        usuario = session.get(Usuario, id_usuario)
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )
        return usuario
    finally:
        session.close()


def _criar_usuario(usuario_dados: UsuarioCreate):
    session = Session()
    try:
        if usuario_dados.email:
            email_existente = (
                session.query(Usuario)
                .filter(Usuario.email == usuario_dados.email)
                .first()
            )
            if email_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"O e-mail '{usuario_dados.email}' já está cadastrado.",
                )

        novo_usuario = Usuario(
            nome=usuario_dados.nome,
            email=usuario_dados.email,
            senha=usuario_dados.senha,
            telefone=usuario_dados.telefone,
            tipo_usuario=usuario_dados.tipo_usuario,
            data_nascimento=usuario_dados.data_nascimento.strftime("%Y-%m-%d"),
            cep=usuario_dados.cep,
            logradouro=usuario_dados.logradouro,
            numero=usuario_dados.numero,
            bairro=usuario_dados.bairro,
            cidade=usuario_dados.cidade,
            estado=usuario_dados.estado,
        )

        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)
        return novo_usuario
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao salvar usuário: {str(e)}",
        )
    finally:
        session.close()


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_dados: UsuarioCreate):
    if usuario_dados.tipo_usuario not in {"aluno", "beneficiario"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O cadastro público permite apenas perfis aluno ou beneficiario.",
        )
    return _criar_usuario(usuario_dados)


@router.post(
    "/admin", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED
)
def criar_admin(
    usuario_dados: UsuarioCreate,
    user_id: int | None = Header(default=None, alias="X-User-Id"),
):
    session = Session()
    try:
        solicitante = session.get(Usuario, user_id) if user_id is not None else None
        if solicitante is None or solicitante.tipo_usuario not in {"root", "admin"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas usuários Root ou Admin podem criar administradores.",
            )
    finally:
        session.close()

    if usuario_dados.tipo_usuario != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta rota permite criar apenas usuários admin.",
        )
    return _criar_usuario(usuario_dados)


@router.post("/login", response_model=UsuarioResponse)
def login(usuario_dados: UsuarioLogin):
    session = Session()
    try:
        usuario = (
            session.query(Usuario)
            .filter(
                Usuario.email == usuario_dados.email,
                Usuario.senha == usuario_dados.senha,
            )
            .first()
        )
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos.",
            )
        return usuario
    finally:
        session.close()
