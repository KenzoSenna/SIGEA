from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from models.base import Base


class TipoReserva(str, PyEnum):
    DIARIA = "diaria"
    SEMESTRAL = "semestral"


class Reserva(Base):
    __tablename__ = "reservas"
    
    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    id_sala = Column(Integer, ForeignKey("salas.id_sala"), nullable=False)
    id_disciplina = Column(Integer, nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    descricao = Column(String(255), nullable=True)
    tipo_reserva = Column(Enum(TipoReserva), nullable=False)
    
    data = Column(Date, nullable=True)
    horario_inicio = Column(Time, nullable=True)
    horario_fim = Column(Time, nullable=True)
    
    data_inicio = Column(Date, nullable=True)
    data_fim = Column(Date, nullable=True)
    dias_semana = Column(JSON, nullable=True)  # ["segunda", "terca", ...]
    horarios = Column(JSON, nullable=True)  # {"segunda": {"inicio": "08:00", "fim": "10:00"}, ...}
    
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Reserva(id={self.id_reserva}, sala={self.id_sala}, tipo='{self.tipo_reserva}')>"
