from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ReservaRequest(BaseModel):
    id_sala: int
    id_disciplina: Optional[int] = None
    descricao: str
    data_inicio: datetime
    data_fim: datetime

    @field_validator("data_fim")
    @classmethod
    def validar_data_fim(cls, v, info):
        if "data_inicio" in info.data and v <= info.data["data_inicio"]:
            raise ValueError("data_fim deve ser maior que data_inicio")
        return v


class ReservaResponse(BaseModel):
    id_reserva: int
    id_sala: int
    id_disciplina: Optional[int] = None
    id_usuario: int
    descricao: Optional[str]
    status: str
    data_inicio: datetime
    data_fim: datetime
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
