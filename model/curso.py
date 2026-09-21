from model.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Curso(Base):
    __tablename__ = "cursos"

    id_curso = Column(Integer, primary_key=True, autoincrement=True)
    nome_curso = Column(String(100), nullable=False)
    carga_horaria = Column(Integer, nullable=False)

    cursas = relationship("Cursa", back_populates="curso")

    def __init__(self, nome_curso, carga_horaria):
        self.nome_curso = nome_curso
        self.carga_horaria = carga_horaria
