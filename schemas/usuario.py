from typing import Literal, Optional

from pydantic import BaseModel, field_validator


class CriarUsuarioRequest(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: Literal["aluno", "professor", "coordenador"]

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validar_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Email inválido")
        return v.lower().strip()

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        return v


class AtualizarUsuarioRequest(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    tipo: Optional[Literal["aluno", "professor", "coordenador"]] = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip() if v else v

    @field_validator("email")
    @classmethod
    def validar_email(cls, v):
        if v is not None:
            if "@" not in v or "." not in v:
                raise ValueError("Email inválido")
            return v.lower().strip()
        return v

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        return v


class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    email: str
    tipo: str
    created_at: str

    class Config:
        from_attributes = True
