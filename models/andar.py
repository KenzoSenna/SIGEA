from sqlalchemy import Column, Integer, Text
from models.base import Base


class Andar(Base):
    __tablename__ = "andar"
    
    id_andar = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False, unique=True)
    pos_x = Column(Text, nullable=False)
    pos_y = Column(Text, nullable=False)
    
    def __repr__(self):
        return f"<Andar(id={self.id_andar}, numero={self.numero})>"
