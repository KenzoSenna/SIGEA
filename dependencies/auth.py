from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from core.security import (
    decode_access_token,
    oauth2_scheme,
    oauth2_scheme_optional,
)
from database.settings import get_db
from models import TokenBloqueado, Usuario

_credenciais_invalidas = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"sucesso": False, "mensagem": "Token inválido ou expirado"},
    headers={"WWW-Authenticate": "Bearer"},
)


def _resolver_usuario(token: str, db: Session) -> Usuario:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        jti = payload.get("jti")

        if user_id is None or jti is None:
            raise _credenciais_invalidas

        user_id = int(user_id)
    except (JWTError, ValueError):
        raise _credenciais_invalidas

    token_revogado = (
        db.query(TokenBloqueado).filter(TokenBloqueado.jti == jti).first()
    )
    if token_revogado:
        raise _credenciais_invalidas

    usuario = (
        db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    )
    if usuario is None:
        raise _credenciais_invalidas

    return usuario


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    return _resolver_usuario(token, db)


def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db),
) -> Usuario | None:
    if token is None:
        return None
    return _resolver_usuario(token, db)
