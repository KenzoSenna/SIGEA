from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base


class Andar(Base):
    __tablename__ = "andares"
    
    id_andar = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    descricao = Column(String(200), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Andar(id={self.id_andar}, numero={self.numero})>"
