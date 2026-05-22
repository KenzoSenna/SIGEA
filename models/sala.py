from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Time
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from models.base import Base


class StatusSala(str, PyEnum):
    ATIVA = "ativa"
    MANUTENCAO = "manutencao"
    INATIVA = "inativa"


class Sala(Base):
    __tablename__ = "salas"
    
    id_sala = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    capacidade = Column(Integer, nullable=False)
    tipo = Column(String(50), nullable=False)
    status = Column(Enum(StatusSala), nullable=False, default=StatusSala.ATIVA)
    horario_inicio = Column(Time, nullable=False)
    horario_fim = Column(Time, nullable=False)
    id_andar = Column(Integer, ForeignKey("andares.id_andar"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Sala(id={self.id_sala}, nome='{self.nome}', capacidade={self.capacidade})>"
