from datetime import time
from typing import Literal, Optional

from pydantic import BaseModel, field_validator


class SalaCreate(BaseModel):
    nome: str
    capacidade: int
    tipo: str
    status: Literal["ativa", "manutencao", "inativa"] = "ativa"
    horario_inicio: time
    horario_fim: time
    id_andar: int

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        if not (1 <= len(v.strip()) <= 50):
            raise ValueError("Nome deve ter entre 1 e 50 caracteres")
        return v.strip()

    @field_validator("capacidade")
    @classmethod
    def validar_capacidade(cls, v):
        if v <= 0:
            raise ValueError("Capacidade deve ser maior que 0")
        return v

    @field_validator("horario_fim")
    @classmethod
    def validar_horarios(cls, v, info):
        if "horario_inicio" in info.data and v <= info.data["horario_inicio"]:
            raise ValueError("horario_fim deve ser maior que horario_inicio")
        return v


class SalaResponse(BaseModel):
    id_sala: int
    nome: str
    capacidade: int
    tipo: str
    status: str
    horario_inicio: time
    horario_fim: time
    id_andar: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
