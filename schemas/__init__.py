"""Schemas Pydantic (DTOs) agrupados por domínio.

Re-exportados aqui para permitir `from schemas import LoginRequest`.
"""
from schemas.andar import AndarResponse, AtualizarAndarRequest, CriarAndarRequest
from schemas.auth import LoginRequest
from schemas.evento import EventoCreate, EventoResponse, UpdateEventoRequest
from schemas.reserva import ReservaRequest, ReservaResponse
from schemas.sala import SalaCreate, SalaResponse
from schemas.usuario import (
    AtualizarUsuarioRequest,
    CriarUsuarioRequest,
    UsuarioResponse,
)

__all__ = [
    "LoginRequest",
    "CriarUsuarioRequest",
    "AtualizarUsuarioRequest",
    "UsuarioResponse",
    "SalaCreate",
    "SalaResponse",
    "CriarAndarRequest",
    "AtualizarAndarRequest",
    "AndarResponse",
    "EventoCreate",
    "UpdateEventoRequest",
    "EventoResponse",
    "ReservaRequest",
    "ReservaResponse",
]
