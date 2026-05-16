from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class StatusSala(str, Enum):
    ATIVA = "ativa"
    MANUTENCAO = "manutencao"


class SalaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=50, description="Nome da sala")
    capacidade: int = Field(..., gt=0, description="Capacidade de pessoas")
    tipo: str = Field(..., max_length=50, description="Tipo de sala (ex: Laboratório, Sala de Aula)")
    status: StatusSala = Field(default=StatusSala.ATIVA, description="Status da sala")
    horario_inicio: str = Field(..., description="Horário de início (HH:MM)")
    horario_fim: str = Field(..., description="Horário de fim (HH:MM)")
    id_andar: int = Field(..., gt=0, description="ID do andar")


class SalaResponse(BaseModel):
    id_sala: int
    nome: str
    capacidade: int
    tipo: str
    status: StatusSala
    horario_inicio: str
    horario_fim: str
    id_andar: int

    class Config:
        from_attributes = True
