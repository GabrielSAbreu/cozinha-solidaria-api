from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from model.base import Base
from model.usuario import Usuario
from model.curso import Curso
from model.cursa import Cursa
from model.beneficio import Beneficio
from model.recebe import Recebe

db = create_engine("sqlite:///database/cozinha_solidaria.db")
Session = sessionmaker(bind=db)

Base.metadata.create_all(db)


def _garantir_coluna_senha():
    """Adiciona a coluna de senha em bancos SQLite já existentes."""
    if "senha" not in {
        column["name"] for column in inspect(db).get_columns("usuarios")
    }:
        with db.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE usuarios ADD COLUMN senha VARCHAR(255) NOT NULL DEFAULT ''"
                )
            )


def _garantir_coluna_data_inicio():
    """Adiciona a data de início em bancos SQLite já existentes."""
    if "data_inicio" not in {
        column["name"] for column in inspect(db).get_columns("cursos")
    }:
        with db.begin() as connection:
            connection.execute(text("ALTER TABLE cursos ADD COLUMN data_inicio DATE"))


def inicializar_usuario_root():
    _garantir_coluna_senha()
    _garantir_coluna_data_inicio()
    session = Session()
    try:
        root_existente = (
            session.query(Usuario).filter(Usuario.tipo_usuario == "root").first()
        )
        if root_existente is None:
            session.add(
                Usuario(
                    nome="Administrador Root",
                    data_nascimento="1970-01-01",
                    tipo_usuario="root",
                    telefone="0000000000",
                    email="root@cozinhasolidaria.org",
                    senha="root123",
                    cep="00000000",
                    logradouro="Endereco inicial",
                    numero="0",
                    bairro="Centro",
                    cidade="Cidade inicial",
                    estado="RS",
                )
            )
            session.commit()
    finally:
        session.close()


inicializar_usuario_root()
