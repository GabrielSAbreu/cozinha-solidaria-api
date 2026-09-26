from model.base import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship


class Curso(Base):
    __tablename__ = "cursos"

    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nome_curso = Column(String(100), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    data_inicio = Column(Date, nullable=False)
    imagem_url = Column(String(2048), nullable=True)

    cursas = relationship("Cursa", back_populates="curso")

    def __init__(self, nome_curso, carga_horaria, data_inicio, imagem_url=None):
        self.nome_curso = nome_curso
        self.carga_horaria = carga_horaria
        self.data_inicio = data_inicio
        self.imagem_url = imagem_url
