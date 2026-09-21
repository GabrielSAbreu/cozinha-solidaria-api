from model.base import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Beneficio(Base):
    __tablename__ = "beneficio"

    id_beneficio = Column(Integer, primary_key=True, autoincrement=True)
    nome_beneficio = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)
    data_entrega = Column(Date, nullable=False)

    recebimentos = relationship("Recebe", back_populates="beneficio")

    def __init__(self, nome_beneficio, descricao, data_entrega):
        self.nome_beneficio = nome_beneficio
        self.descricao = descricao
        self.data_entrega = data_entrega
