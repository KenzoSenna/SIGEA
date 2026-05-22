from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Time
from enum import Enum as PyEnum
from models.base import Base


class StatusSala(str, PyEnum):
    ATIVA = "ativa"
    MANUTENCAO = "manutencao"


class Sala(Base):
    __tablename__ = "sala"
    
    id_sala = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    capacidade = Column(Integer, nullable=True)
    tipo = Column(String(50), nullable=True)
    status = Column(Enum(StatusSala), nullable=False, default=StatusSala.ATIVA)
    horario_inicio = Column(Time, nullable=True)
    horario_fim = Column(Time, nullable=True)
    id_andar = Column(Integer, ForeignKey("andar.id_andar"), nullable=False)
    
    def __repr__(self):
        return f"<Sala(id={self.id_sala}, nome='{self.nome}', capacidade={self.capacidade})>"
