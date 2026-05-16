from fastapi import FastAPI, APIRouter, HTTPException
from datetime import date, time
from pydantic import BaseModel, model_validator, field_validator
from typing import Union, Literal, List, Dict, Optional
import uvicorn

app = FastAPI()
router = APIRouter(tags=["Sistema de reserva"])
 
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
   
EMAIL = "usuario@email.com"
SENHA = "senha123"
salas = [201, 202, 204]
reservas = {}
contador_reserva = 0

# Dados de usuários
usuarios = {}
contador_usuario = 0
emails_cadastrados = set()

def _verificar_conflito(id_sala: int, dados_nova: Union[ReservaDiaria, ReservaSemestral], tipo: str) -> bool:
    """Verifica se há sobreposição de horários na mesma sala"""
    for reserva in reservas.values():
        if reserva['id_sala'] != id_sala:
            continue
        
        if tipo == "diaria" and reserva['tipo_reserva'] == "diaria":
            if reserva['data'] == dados_nova.data:
                
                if not (dados_nova.horario_fim <= reserva['horario_inicio'] or 
                       dados_nova.horario_inicio >= reserva['horario_fim']):
                    return True
    
    return False

@router.post("/login", summary="Fazer login")
async def login(dados: LoginRequest):
    if dados.email != EMAIL:
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})
    if dados.senha != SENHA:
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})
    return {"sucesso": True, "mensagem": "Autenticação realizada com sucesso", "email": dados.email, "sessao": "autenticada"}

@router.post("/reservas", summary="Realizar reserva de sala")
async def create_reserva(dados: ReservaRequest):
    global contador_reserva
    
    if dados.id_sala not in salas:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Sala não encontrada"})
    
    if _verificar_conflito(dados.id_sala, dados.detalhes, dados.tipo_reserva):
        raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Horário indisponível nesta sala"})
    
    contador_reserva += 1
    id_reserva = contador_reserva
    
    if dados.tipo_reserva == "diaria":
        reservas[id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data": str(dados.detalhes.data),
            "horario_inicio": str(dados.detalhes.horario_inicio),
            "horario_fim": str(dados.detalhes.horario_fim),
        }
    elif dados.tipo_reserva == "semestral":
        reservas[id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data_inicio": str(dados.detalhes.data_inicio),
            "data_fim": str(dados.detalhes.data_fim),
            "dias_semana": dados.detalhes.dias_semana,
            "horarios": {dia: {"inicio": str(h["inicio"]), "fim": str(h["fim"])} 
                        for dia, h in dados.detalhes.horarios.items()},
        }

    return {
        "sucesso": True, 
        "mensagem": f"Reserva {dados.tipo_reserva} realizada com sucesso!",
        "id_reserva": id_reserva,
        "reserva": reservas[id_reserva]
    }

@router.get("/reservas", summary="Listar todas as reservas")
async def listar_reservas():
    return {
        "sucesso": True,
        "total": len(reservas),
        "reservas": reservas
    }

@router.get("/reservas/{id_reserva}", summary="Obter detalhes de uma reserva")
async def obter_reserva(id_reserva: int):
    if id_reserva not in reservas:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Reserva não encontrada"})
    return {
        "sucesso": True,
        "reserva": reservas[id_reserva]
    }

@router.delete("/reservas/{id_reserva}", summary="Cancelar uma reserva")
async def cancelar_reserva(id_reserva: int):
    if id_reserva not in reservas:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Reserva não encontrada"})
    
    reserva_removida = reservas.pop(id_reserva)
    return {
        "sucesso": True,
        "mensagem": "Reserva cancelada com sucesso",
        "reserva_removida": reserva_removida
    }

# ========== ROTAS DE USUÁRIOS ==========

router_usuarios = APIRouter(tags=["Usuários"])

@router_usuarios.post("/usuarios", summary="Criar novo usuário")
async def criar_usuario(dados: CriarUsuarioRequest):
    global contador_usuario
    
    if dados.email in emails_cadastrados:
        raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Email já cadastrado"})
    
    contador_usuario += 1
    id_usuario = contador_usuario
    
    usuarios[id_usuario] = {
        "id_usuario": id_usuario,
        "nome": dados.nome,
        "email": dados.email,
        "senha": dados.senha,
        "tipo": dados.tipo,
        "created_at": str(__import__('datetime').datetime.now().isoformat())
    }
    
    emails_cadastrados.add(dados.email)
    
    return {
        "sucesso": True,
        "mensagem": "Usuário criado com sucesso",
        "id_usuario": id_usuario,
        "usuario": {
            "id_usuario": usuarios[id_usuario]["id_usuario"],
            "nome": usuarios[id_usuario]["nome"],
            "email": usuarios[id_usuario]["email"],
            "tipo": usuarios[id_usuario]["tipo"],
            "created_at": usuarios[id_usuario]["created_at"]
        }
    }

@router_usuarios.get("/usuarios", summary="Listar todos os usuários")
async def listar_usuarios():
    lista_usuarios = []
    for usuario in usuarios.values():
        lista_usuarios.append({
            "id_usuario": usuario["id_usuario"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "tipo": usuario["tipo"],
            "created_at": usuario["created_at"]
        })
    
    return {
        "sucesso": True,
        "total": len(usuarios),
        "usuarios": lista_usuarios
    }

@router_usuarios.get("/usuarios/{id_usuario}", summary="Obter detalhes de um usuário")
async def obter_usuario(id_usuario: int):
    if id_usuario not in usuarios:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})
    
    usuario = usuarios[id_usuario]
    return {
        "sucesso": True,
        "usuario": {
            "id_usuario": usuario["id_usuario"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "tipo": usuario["tipo"],
            "created_at": usuario["created_at"]
        }
    }

@router_usuarios.delete("/usuarios/{id_usuario}", summary="Deletar um usuário")
async def deletar_usuario(id_usuario: int):
    if id_usuario not in usuarios:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})
    
    usuario_removido = usuarios.pop(id_usuario)
    emails_cadastrados.discard(usuario_removido["email"])
    
    return {
        "sucesso": True,
        "mensagem": "Usuário deletado com sucesso",
        "usuario_removido": {
            "id_usuario": usuario_removido["id_usuario"],
            "nome": usuario_removido["nome"],
            "email": usuario_removido["email"]
        }
    }
        
app.include_router(router)
app.include_router(router_usuarios)
 
if __name__ == "__main__":
    uvicorn.run("_routes:app", host="localhost", port=8000, reload=True)