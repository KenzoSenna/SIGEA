from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import LoginRequest
from core.security import (
    create_access_token,
    decode_access_token,
    oauth2_scheme,
    verify_password,
)
from services.usuarios import get_user_by_email
from dependencies.auth import get_current_user
from database.settings import get_db
from models import Usuario, TokenBloqueado

router = APIRouter(tags=["Auth"])

@router.post("/login", summary="Fazer login")
async def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = get_user_by_email(dados.email, db)
    if usuario is None or not verify_password(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})

    access_token = create_access_token({
        "sub": str(usuario.id_usuario),
        "email": usuario.email,
        "tipo": usuario.tipo
    })

    return {
        "sucesso": True,
        "mensagem": "Autenticação realizada com sucesso",
        "sessao": "autenticada",
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "email": usuario.email,
            "tipo": usuario.tipo
        },
        "ativo": 1
    }


@router.post(
    "/logout",
    summary="Fazer logout"
)
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        payload = decode_access_token(token)

        jti = payload.get("jti")
        exp = payload.get("exp")

        token_bloqueado = TokenBloqueado(
            jti=jti,
            expira_em=datetime.fromtimestamp(exp, tz=timezone.utc).replace(tzinfo=None)
        )

        db.add(token_bloqueado)
        db.commit()

        return {
            "sucesso": True,
            "mensagem": "Logout realizado com sucesso",
            "sessao": "finalizada",
            "usuario_id": current_user.id_usuario,
            "ativo": 0
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )
