from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Cursa(Base):
    __tablename__ = "cursa"

    fk_usuario_id_usuario = Column(
        Integer, ForeignKey("usuarios.id_usuario"), nullable=False, primary_key=True
    )

    fk_curso_id_curso = Column(
        Integer, ForeignKey("cursos.id_curso"), nullable=False, primary_key=True
    )

    status = Column(String(50), nullable=False)

    usuario = relationship("Usuario", back_populates="cursas")
    curso = relationship("Curso", back_populates="cursas")
