import uuid
from datetime import date, datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from database.settings import settings, SessionLocal, get_db
from models import Usuario, Reserva, Evento, TokenBloqueado, Sala, StatusSala
from sqlalchemy.orm import Session


def tratar_integrity_error(e) -> str:
    msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
    if "1062" in msg or "Duplicate entry" in msg:
        return "Registro duplicado — este valor já existe no sistema"
    if "1452" in msg or "foreign key constraint" in msg.lower():
        return "Referência inválida — registro relacionado não encontrado"
    return "Violação de integridade de dados"


def converter_para_datetime(data: date, hora) -> datetime:
    if isinstance(hora, str):
        hora = datetime.strptime(hora, "%H:%M:%S").time()
    return datetime.combine(data, hora)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)

oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/login",
    auto_error=False
)

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or
        timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.jwt_algorithm
    )


def get_user_by_email(
    email: str,
    db: Session = None
):

    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False

    try:
        usuario = (
            db.query(Usuario)
            .filter(Usuario.email == email.lower())
            .first()
        )

        return usuario

    finally:
        if should_close:
            db.close()


def _autenticar_token(token: str, db: Session) -> Usuario:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "sucesso": False,
            "mensagem": "Token inválido ou expirado"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("sub")
        jti = payload.get("jti")

        if user_id is None or jti is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    token_revogado = (
        db.query(TokenBloqueado)
        .filter(TokenBloqueado.jti == jti)
        .first()
    )

    if token_revogado:
        raise credentials_exception

    usuario = (
        db.query(Usuario)
        .filter(Usuario.id_usuario == user_id)
        .first()
    )

    if usuario is None:
        raise credentials_exception

    return usuario


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:

    return _autenticar_token(token, db)


def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme_optional),
    db: Session = Depends(get_db)
) -> Usuario | None:

    if token is None:
        return None

    return _autenticar_token(token, db)


def exigir_tipo(usuario: Usuario, *tipos_permitidos: str):

    if usuario.tipo not in tipos_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "sucesso": False,
                "mensagem": f"Permissão insuficiente — ação restrita a: {', '.join(tipos_permitidos)}"
            }
        )


def exigir_dono_ou_coordenador(usuario: Usuario, id_dono: int | None, acao: str):

    if usuario.tipo == "coordenador":
        return

    if id_dono is None or usuario.id_usuario != id_dono:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "sucesso": False,
                "mensagem": f"Permissão insuficiente — apenas o responsável ou um coordenador pode {acao}"
            }
        )


def verificar_conflito(
    id_sala: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session,
    exclude_id: int = None,
    exclude_tipo: str = "reserva"
) -> bool:

    reservas = db.query(Reserva.id_reserva).filter(
        Reserva.id_sala == id_sala,
        Reserva.data_inicio < data_fim,
        Reserva.data_fim > data_inicio,
    )

    if exclude_tipo == "reserva" and exclude_id is not None:
        reservas = reservas.filter(Reserva.id_reserva != exclude_id)

    if reservas.first() is not None:
        return True

    eventos = db.query(Evento.id_evento).filter(
        Evento.id_sala == id_sala,
        Evento.data_inicio < data_fim,
        Evento.data_fim > data_inicio,
    )

    if exclude_tipo == "evento" and exclude_id is not None:
        eventos = eventos.filter(Evento.id_evento != exclude_id)

    return eventos.first() is not None


def obter_sala_disponivel(
    id_sala: int,
    db: Session
) -> Sala:

    sala = db.query(Sala).filter(Sala.id_sala == id_sala).first()

    if not sala:
        raise HTTPException(
            status_code=404,
            detail={"sucesso": False, "mensagem": f"Sala {id_sala} não encontrada"}
        )

    if sala.status != StatusSala.ATIVA:
        raise HTTPException(
            status_code=409,
            detail={
                "sucesso": False,
                "mensagem": f"Sala {id_sala} não está disponível (status: {sala.status.value})"
            }
        )

    return sala


def purge_expired_tokens(db: Session) -> int:

    removidos = (
        db.query(TokenBloqueado)
        .filter(TokenBloqueado.expira_em < datetime.now(timezone.utc).replace(tzinfo=None))
        .delete(synchronize_session=False)
    )

    db.commit()
    return removidos


def seed_default_user(
    db: Session = None
):

    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False

    try:

        existing = (
            db.query(Usuario)
            .filter(
                Usuario.email == "usuario@email.com"
            )
            .first()
        )

        # Usuário seed é o coordenador de bootstrap — sem ele não existiria
        # nenhum coordenador para criar outros coordenadores e gerir salas/andares.
        if not existing:

            usuario = Usuario(
                nome="Usuário Padrão",
                email="usuario@email.com",
                senha_hash=get_password_hash("senha123"),
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