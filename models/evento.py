from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from models.base import Base


class Evento(Base):
    __tablename__ = "evento"
    
    id_evento = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(String(255), nullable=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    tipo = Column(String(50), nullable=True)
    destaque = Column(Boolean, nullable=False, default=False)
    id_sala = Column(Integer, ForeignKey("sala.id_sala"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    def __repr__(self):
        return f"<Evento(id={self.id_evento}, titulo='{self.titulo}', data_inicio='{self.data_inicio}')>"
