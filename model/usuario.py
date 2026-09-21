from model.base import Base
from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    data_nascimento = Column(String(10), nullable=False)
    tipo_usuario = Column(String(50), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False, default="")
    cep = Column(String(10), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=False)
    bairro = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(50), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "tipo_usuario IN ('root', 'admin', 'aluno', 'beneficiario')",
            name="ck_usuario_tipo_usuario",
        ),
    )

    cursas = relationship("Cursa", back_populates="usuario")
    recebimentos = relationship("Recebe", back_populates="usuario")

    def __init__(
        self,
        nome,
        data_nascimento,
        tipo_usuario,
        telefone,
        email,
        senha,
        cep,
        logradouro,
        numero,
        bairro,
        cidade,
        estado,
    ):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.tipo_usuario = tipo_usuario
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
