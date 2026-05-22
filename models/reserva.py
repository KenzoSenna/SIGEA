from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    Text
)

from sqlalchemy.sql import func
from enum import Enum as PyEnum

from models.base import Base


class StatusReserva(str, PyEnum):
    ATIVA = "ativa"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluida"

class Reserva(Base):
    __tablename__ = "reserva"

    id_reserva = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    data_inicio = Column(
        DateTime,
        nullable=False
    )

    data_fim = Column(
        DateTime,
        nullable=False
    )

    descricao = Column(
        Text,
        nullable=True
    )

    status = Column(
        Enum(StatusReserva),
        nullable=False,
        default=StatusReserva.ATIVA
    )

    id_sala = Column(
        Integer,
        ForeignKey("sala.id_sala", ondelete="CASCADE"),
        nullable=False
    )

    id_usuario = Column(
        Integer,
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False
    )

    id_disciplina = Column(
        Integer,
        ForeignKey("disciplina.id_disciplina", ondelete="SET NULL"),
        nullable=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    def __repr__(self):
        return (
            f"<Reserva("
            f"id={self.id_reserva}, "
            f"sala={self.id_sala}, "
            f"status='{self.status}'"
            f")>"
        )