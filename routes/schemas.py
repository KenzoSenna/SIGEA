from datetime import date, time
from pydantic import BaseModel, model_validator, field_validator
from typing import Union, Literal, List, Dict, Optional


# ==================== AUTENTICAÇÃO ====================
class LoginRequest(BaseModel):
    email: str
    senha: str


# ==================== USUÁRIOS ====================
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


class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    email: str
    tipo: str
    created_at: str

    class Config:
        from_attributes = True


# ==================== SALAS ====================
class SalaCreate(BaseModel):
    nome: str = field_validator('nome')(lambda v: v if len(v) >= 1 and len(v) <= 50 else None)
    capacidade: int
    tipo: str
    status: Literal["ativa", "manutencao", "inativa"] = "ativa"
    horario_inicio: time
    horario_fim: time
    id_andar: int
    
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


# ==================== EVENTOS ====================
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


# ==================== RESERVAS ====================
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
    id_disciplina: int
    descricao: str
    tipo_reserva: Literal["diaria", "semestral"]
    detalhes: Union[ReservaDiaria, ReservaSemestral]

    @model_validator(mode='after')
    def verificar_tipo_detalhes(self):
        if self.tipo_reserva == "diaria" and not isinstance(self.detalhes, ReservaDiaria):
            raise ValueError("Para 'tipo_reserva' igual a 'diaria', insira os campos de ReservaDiaria.")
        if self.tipo_reserva == "semestral" and not isinstance(self.detalhes, ReservaSemestral):
            raise ValueError("Para 'tipo_reserva' igual a 'semestral', insira os campos de ReservaSemestral.")
        return self


class ReservaResponse(BaseModel):
    id_reserva: int
    id_sala: int
    id_disciplina: int
    id_usuario: int
    descricao: Optional[str]
    tipo_reserva: str
    data: Optional[date] = None
    horario_inicio: Optional[time] = None
    horario_fim: Optional[time] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    dias_semana: Optional[List[str]] = None
    horarios: Optional[dict] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

