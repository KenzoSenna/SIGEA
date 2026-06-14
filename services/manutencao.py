from datetime import datetime, timezone

from sqlalchemy.orm import Session

from core.security import get_password_hash
from database.settings import SessionLocal
from models import TokenBloqueado, Usuario

SEED_EMAIL = "usuario@email.com"
SEED_SENHA = "senha123"


def purge_expired_tokens(db: Session) -> int:
    
    removidos = (
        db.query(TokenBloqueado)
        .filter(TokenBloqueado.expira_em < datetime.now(timezone.utc).replace(tzinfo=None))
        .delete(synchronize_session=False)
    )
    db.commit()
    return removidos


def seed_default_user(db: Session | None = None) -> None:
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False

    try:
        existing = (
            db.query(Usuario).filter(Usuario.email == SEED_EMAIL).first()
        )

        if not existing:
            usuario = Usuario(
                nome="Usuário Padrão",
                email=SEED_EMAIL,
                senha_hash=get_password_hash(SEED_SENHA),
                tipo="coordenador",
            )
            db.add(usuario)
            db.commit()
        elif existing.tipo != "coordenador":
            existing.tipo = "coordenador"
            db.commit()
    finally:
        if should_close:
            db.close()
