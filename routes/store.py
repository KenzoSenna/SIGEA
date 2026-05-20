from datetime import datetime, timedelta, time as dt_time
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose import JWTError, jwt
from typing import Union
from database.settings import settings

# demo
EMAIL = "usuario@email.com"
SENHA = "senha123"
SALAS = [201, 202, 204]
reservas: dict = {}
contador_reserva = 0

usuarios: dict = {}
contador_usuario = 0
emails_cadastrados = set()

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


def get_user_by_email(email: str):
    for usuario in usuarios.values():
        if usuario["email"].lower() == email.lower():
            return usuario
    return None


from fastapi import Depends


def get_current_user(token: str = Depends(oauth2_scheme)):
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

    usuario = usuarios.get(user_id)
    if usuario is None:
        raise credentials_exception
    return usuario


def _seed_default_user():
    global contador_usuario
    contador_usuario += 1
    usuarios[contador_usuario] = {
        "id_usuario": contador_usuario,
        "nome": "Usuário Padrão",
        "email": EMAIL,
        "senha_hash": get_password_hash(SENHA),
        "tipo": "professor",
        "created_at": datetime.now().isoformat()
    }
    emails_cadastrados.add(EMAIL)


_seed_default_user()


def _verificar_conflito(id_sala: int, dados_nova: Union[object, object], tipo: str) -> bool:
    """Verifica se há sobreposição de horários na mesma sala"""
    for reserva in reservas.values():
        if reserva['id_sala'] != id_sala:
            continue
        
        if tipo == "diaria" and reserva.get('tipo_reserva') == "diaria":
            # reserva['data'] is stored as string
            if reserva['data'] == str(dados_nova.data):
                inicio = dt_time.fromisoformat(reserva['horario_inicio'])
                fim = dt_time.fromisoformat(reserva['horario_fim'])
                if not (dados_nova.horario_fim <= inicio or 
                       dados_nova.horario_inicio >= fim):
                    return True
    return False
