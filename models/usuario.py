from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
from models.base import Base


class TipoUsuario(str, PyEnum):
    ALUNO = "aluno"
    PROFESSOR = "professor"
    COORDENADOR = "coordenador"


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha = Column(Text, nullable=False)
    senha_hash = Column(String(255), nullable=True)
    tipo = Column(Enum(TipoUsuario), nullable=False, default=TipoUsuario.ALUNO)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome='{self.nome}', email='{self.email}')>"
