from datetime import date, time
from typing import Optional

from pydantic import BaseModel, field_validator


class EventoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data: date
    hora_inicio: time
    hora_fim: time
    id_sala: int

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        v = v.strip()
        if not (1 <= len(v) <= 100):
            raise ValueError("Nome deve ter entre 1 e 100 caracteres")
        return v

    @field_validator("hora_fim")
    @classmethod
    def validar_horas(cls, v, info):
        if "hora_inicio" in info.data and v <= info.data["hora_inicio"]:
            raise ValueError("hora_fim deve ser maior que hora_inicio")
        return v


class UpdateEventoRequest(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fim: Optional[time] = None
    id_sala: Optional[int] = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        if v is not None:
            if len(v.strip()) < 1 or len(v) > 100:
                raise ValueError("Nome deve ter entre 1 e 100 caracteres")
            return v.strip()
        return v

    @field_validator("hora_fim")
    @classmethod
    def validar_horas(cls, v, info):
        if v is not None and "hora_inicio" in info.data and info.data["hora_inicio"] is not None:
            if v <= info.data["hora_inicio"]:
                raise ValueError("hora_fim deve ser maior que hora_inicio")
        return v


class EventoResponse(BaseModel):
    id_evento: int
    nome: str
    descricao: Optional[str]
    data: date
    hora_inicio: time
    hora_fim: time
    id_sala: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
