from datetime import date, time
from pydantic import BaseModel, model_validator, field_validator
from typing import Union, Literal, List, Dict

class LoginRequest(BaseModel):
    email: str
    senha: str

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
