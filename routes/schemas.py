from datetime import date, time, datetime
from pydantic import BaseModel, model_validator, field_validator
from typing import Union, Literal, List, Dict, Optional


class LoginRequest(BaseModel):
    email: str
    senha: str


class CriarUsuarioRequest(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: Literal["aluno", "professor", "coordenador"]
    
    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError("Email inválido")
        return v.lower().strip()
    
    @field_validator('senha')
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

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if v is not None and len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip() if v else v

    @field_validator('email')
    @classmethod
    def validar_email(cls, v):
        if v is not None:
            if '@' not in v or '.' not in v:
                raise ValueError("Email inválido")
            return v.lower().strip()
        return v

    @field_validator('senha')
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

class SalaCreate(BaseModel):
    nome: str
    capacidade: int
    tipo: str
    status: Literal["ativa", "manutencao", "inativa"] = "ativa"
    horario_inicio: time
    horario_fim: time
    id_andar: int

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if not (1 <= len(v.strip()) <= 50):
            raise ValueError("Nome deve ter entre 1 e 50 caracteres")
        return v.strip()

    @field_validator('capacidade')
    @classmethod
    def validar_capacidade(cls, v):
        if v <= 0:
            raise ValueError("Capacidade deve ser maior que 0")
        return v

    @field_validator('horario_fim')
    @classmethod
    def validar_horarios(cls, v, info):
        if 'horario_inicio' in info.data and v <= info.data['horario_inicio']:
            raise ValueError("horario_fim deve ser maior que horario_inicio")
        return v


class SalaResponse(BaseModel):
    id_sala: int
    nome: str
    capacidade: int
    tipo: str
    status: str
    horario_inicio: time
    horario_fim: time
    id_andar: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class CriarAndarRequest(BaseModel):
    numero: int
    pos_x: str
    pos_y: str
    
    @field_validator('numero')
    @classmethod
    def validar_numero(cls, v):
        if v < 0:
            raise ValueError("Número do andar não pode ser negativo")
        return v
    
    @field_validator('pos_x', 'pos_y')
    @classmethod
    def validar_posicoes(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Posições não podem estar vazias")
        return v.strip()


class AtualizarAndarRequest(BaseModel):
    numero: Optional[int] = None
    pos_x: Optional[str] = None
    pos_y: Optional[str] = None
    
    @field_validator('numero')
    @classmethod
    def validar_numero(cls, v):
        if v is not None and v < 0:
            raise ValueError("Número do andar não pode ser negativo")
        return v
    
    @field_validator('pos_x', 'pos_y')
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


class EventoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    data: date
    hora_inicio: time
    hora_fim: time
    id_sala: int
    
    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if len(v.strip()) < 1 or len(v) > 100:
            raise ValueError("Nome deve ter entre 1 e 100 caracteres")
        return v.strip()
    
    @field_validator('hora_fim')
    @classmethod
    def validar_horas(cls, v, info):
        if 'hora_inicio' in info.data and v <= info.data['hora_inicio']:
            raise ValueError("hora_fim deve ser maior que hora_inicio")
        return v


class EventoResponse(BaseModel):
    id_evento: int
    nome: str
    descricao: Optional[str]
    data: date
    hora_inicio: time
    hora_fim: time
    id_sala: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateEventoRequest(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fim: Optional[time] = None
    id_sala: Optional[int] = None
    
    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v):
        if v is not None:
            if len(v.strip()) < 1 or len(v) > 100:
                raise ValueError("Nome deve ter entre 1 e 100 caracteres")
            return v.strip()
        return v
    
    @field_validator('hora_fim')
    @classmethod
    def validar_horas(cls, v, info):
        if v is not None and 'hora_inicio' in info.data and info.data['hora_inicio'] is not None:
            if v <= info.data['hora_inicio']:
                raise ValueError("hora_fim deve ser maior que hora_inicio")
        return v


class ReservaDiaria(BaseModel):
    data: date
    horario_inicio: time
    horario_fim: time
    
    @field_validator('horario_fim')
    @classmethod
    def validar_horario_fim(cls, v, info):
        if 'horario_inicio' in info.data and v <= info.data['horario_inicio']:
            raise ValueError("horario_fim deve ser maior que horario_inicio")
        return v


class ReservaSemestral(BaseModel):
    data_inicio: date
    data_fim: date
    dias_semana: List[Literal["segunda","terca","quarta","quinta","sexta","sabado","domingo"]]
    horarios: Dict[Literal["segunda","terca","quarta","quinta","sexta","sabado","domingo"], 
                   Dict[Literal["inicio", "fim"], time]]
    
    @field_validator('data_fim')
    @classmethod
    def validar_data_fim(cls, v, info):
        if 'data_inicio' in info.data and v <= info.data['data_inicio']:
            raise ValueError("data_fim deve ser maior que data_inicio")
        return v
    
    @field_validator('horarios')
    @classmethod
    def validar_horarios(cls, v, info):
        for dia, horarios in v.items():
            if horarios['fim'] <= horarios['inicio']:
                raise ValueError(f"horario_fim deve ser maior que horario_inicio para {dia}")
        return v


class ReservaRequest(BaseModel):
    id_sala: int
    id_disciplina: Optional[int] = None
    descricao: str
    data_inicio: datetime
    data_fim: datetime

    @field_validator('data_fim')
    @classmethod
    def validar_data_fim(cls, v, info):
        if 'data_inicio' in info.data and v <= info.data['data_inicio']:
            raise ValueError("data_fim deve ser maior que data_inicio")
        return v


class ReservaResponse(BaseModel):
    id_reserva: int
    id_sala: int
    id_disciplina: Optional[int] = None
    id_usuario: int
    descricao: Optional[str]
    status: str
    data_inicio: datetime
    data_fim: datetime
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

