from typing import Optional

from pydantic import BaseModel, field_validator


class CriarAndarRequest(BaseModel):
    numero: int
    pos_x: str
    pos_y: str

    @field_validator("numero")
    @classmethod
    def validar_numero(cls, v):
        if v < 0:
            raise ValueError("Número do andar não pode ser negativo")
        return v

    @field_validator("pos_x", "pos_y")
    @classmethod
    def validar_posicoes(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Posições não podem estar vazias")
        return v.strip()


class AtualizarAndarRequest(BaseModel):
    numero: Optional[int] = None
    pos_x: Optional[str] = None
    pos_y: Optional[str] = None

    @field_validator("numero")
    @classmethod
    def validar_numero(cls, v):
        if v is not None and v < 0:
            raise ValueError("Número do andar não pode ser negativo")
        return v

    @field_validator("pos_x", "pos_y")
    @classmethod
    def validar_posicoes(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Posições não podem estar vazias")
        return v.strip() if v else v


class AndarResponse(BaseModel):
    id_andar: int
    numero: int
    pos_x: str
    pos_y: str

    class Config:
        from_attributes = True
