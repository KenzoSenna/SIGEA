from datetime import datetime, timedelta, time as dt_time
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from typing import Union
from database.settings import settings, SessionLocal, get_db
from models import Usuario, TipoReserva
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)


def get_user_by_email(email: str, db: Session = None):
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        usuario = db.query(Usuario).filter(Usuario.email == email.lower()).first()
        return usuario
    finally:
        if should_close:
            db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"sucesso": False, "mensagem": "Token inválido ou expirado"},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, ValueError):
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if usuario is None:
        raise credentials_exception
    return usuario


def verificar_conflito(id_sala: int, dados_nova: Union[object, object], tipo: str, db: Session) -> bool:
    """Verifica se há sobreposição de horários na mesma sala"""
    from models import Reserva
    
    reservas = db.query(Reserva).filter(Reserva.id_sala == id_sala).all()
    
    for reserva in reservas:
        if tipo == "diaria" and reserva.tipo_reserva == TipoReserva.DIARIA:
            if reserva.data == dados_nova.data:
                if not (dados_nova.horario_fim <= reserva.horario_inicio or 
                       dados_nova.horario_inicio >= reserva.horario_fim):
                    return True
        elif tipo == "semestral" and reserva.tipo_reserva == TipoReserva.SEMESTRAL:
            # Verificação mais complexa para semestrais
            if not (dados_nova.data_fim < reserva.data_inicio or 
                   dados_nova.data_inicio > reserva.data_fim):
                # Há sobreposição de datas
                if any(dia in reserva.dias_semana for dia in dados_nova.dias_semana):
                    return True
    return False


def seed_default_user(db: Session = None):
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False
    
    try:
        existing = db.query(Usuario).filter(Usuario.email == "usuario@email.com").first()
        if not existing:
            usuario = Usuario(
                nome="Usuário Padrão",
                email="usuario@email.com",
                senha_hash=get_password_hash("senha123"),
                tipo=TipoReserva.PROFESSOR if hasattr(TipoReserva, 'PROFESSOR') else "professor",
            )
            db.add(usuario)
            db.commit()
    finally:
        if should_close:
            db.close()

    return False
