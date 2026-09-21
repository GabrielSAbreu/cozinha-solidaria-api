from model.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Recebe(Base):
    __tablename__ = "recebe"

    fk_usuario_id_usuario = Column(
        Integer, ForeignKey("usuarios.id_usuario"), nullable=False, primary_key=True
    )

    fk_beneficio_id_beneficio = Column(
        Integer, ForeignKey("beneficio.id_beneficio"), nullable=False, primary_key=True
    )

    status = Column(String(50), nullable=False)

    usuario = relationship("Usuario", back_populates="recebimentos")
    beneficio = relationship("Beneficio", back_populates="recebimentos")
