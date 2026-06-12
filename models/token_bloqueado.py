from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from models.base import Base


class TokenBloqueado(Base):
    __tablename__ = "token_bloqueado"

    jti = Column(String(36), primary_key=True)
    expira_em = Column(DateTime, nullable=False)
    bloqueado_em = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f"<TokenBloqueado(jti='{self.jti}', expira_em='{self.expira_em}')>"
