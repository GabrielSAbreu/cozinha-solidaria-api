from fastapi import Header, HTTPException, status

from model import Session
from model.usuario import Usuario


def verificar_permissao(
    user_id: int | None, papeis: set[str], mensagem: str
) -> Usuario:
    session = Session()
    try:
        usuario = session.get(Usuario, user_id) if user_id is not None else None
        if usuario is None or usuario.tipo_usuario.lower() not in papeis:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=mensagem)
        return usuario
    finally:
        session.close()


def usuario_com_permissao_admin(
    user_id: int | None = Header(default=None, alias="X-User-Id"),
) -> Usuario:
    return verificar_permissao(
        user_id,
        {"root", "admin"},
        "Apenas usuários Root ou Admin possuem permissão para esta operação.",
    )


def usuario_root(
    user_id: int | None = Header(default=None, alias="X-User-Id"),
) -> Usuario:
    return verificar_permissao(
        user_id,
        {"root"},
        "Apenas o usuário Root possui permissão para exclusão de registros.",
    )
