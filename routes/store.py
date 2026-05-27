import uuid
from datetime import date, datetime, time as time_type, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from database.settings import settings, SessionLocal, get_db
from models import Usuario, Reserva, Evento, TokenBloqueado
from sqlalchemy.orm import Session


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

    expire = datetime.utcnow() + (
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


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

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


def verificar_conflito(
    id_sala: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session,
    exclude_id: int = None,
    exclude_tipo: str = "reserva"
) -> bool:

    reservas = (
        db.query(Reserva)
        .filter(Reserva.id_sala == id_sala)
        .all()
    )

    for reserva in reservas:

        if exclude_tipo == "reserva" and exclude_id is not None and reserva.id_reserva == exclude_id:
            continue

        if data_inicio < reserva.data_fim and data_fim > reserva.data_inicio:
            return True

    eventos = (
        db.query(Evento)
        .filter(Evento.id_sala == id_sala)
        .all()
    )

    for evento in eventos:

        if exclude_tipo == "evento" and exclude_id is not None and evento.id_evento == exclude_id:
            continue

        if data_inicio < evento.data_fim and data_fim > evento.data_inicio:
            return True

    return False


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

        if not existing:

            usuario = Usuario(
                nome="Usuário Padrão",
                email="usuario@email.com",
                senha_hash=get_password_hash("senha123"),
                tipo="professor",
            )

            db.add(usuario)
            db.commit()

    finally:
        if should_close:
            db.close()