from enum import Enum
from pydantic import BaseModel, Field

class NomeBloco(str, Enum):
    COORDENACAO = "Bloco de Coordenação"
    BLOCO_A = "Bloco A - Bloco Principal"
    BLOCO_B = "Bloco B - Bloco de Laboratórios"

class NomeAndar(str, Enum):
    TERREO = "Térreo"
    PRIMEIRO_ANDAR = "1º Andar"

class AndarCreate(BaseModel):
    nome: NomeAndar = Field(..., description="Nome do andar válido", examples=[NomeAndar.TERREO])
    bloco: NomeBloco = Field(..., description="Nome do bloco válido", examples=[NomeBloco.BLOCO_A])

class AndarResponse(BaseModel):
    id_andar: int
    nome: NomeAndar
    bloco: NomeBloco

    class Config:
        from_attributes = True
