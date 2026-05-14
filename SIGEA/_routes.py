from fastapi import FastAPI, APIRouter, HTTPException
from datetime import datetime, date, time
from pydantic import BaseModel
import uvicorn
 
app = FastAPI()
router = APIRouter(prefix="/auth", tags=["Autenticação"])
 
class LoginRequest(BaseModel):
    email: str
    senha: str
    role: int

class ReservaSemestral(BaseModel):
    data_inicio: date
    data_fim: date
    horario_inicio: time
    horario_fim: time
class ReservaDiaria(BaseModel):
    data: date
    horario_inicio: time
    horario_fim: time

class ReservaRequest(BaseModel):
    id_reserva: int
    id_sala: int
    semestral: bool
    id_disciplina: int
    datetime_inicio: datetime
    datetime_fim: datetime
    descricao: str


EMAIL = "usuario@email.com"
SENHA = "senha123"
ROLE_PROFESSOR = 0
ROLE_ALUNO = 1
salas = {}
reservas = {}

@router.post("/login", summary="Fazer login")
async def login(dados: LoginRequest):
    if dados.email != EMAIL:
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})
    if dados.senha != SENHA:
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})
    return {"sucesso": True, "mensagem": "Autenticação realizada com sucesso", "email": dados.email, "sessao": "autenticada"}

@router.post("/reservas", summary="Realizar reserva de sala")
async def create_reserva(dados: ReservaRequest):
    if dados.id_sala in salas:
        if dados.semestral == True:
            pass
        reservas[dados.id_reserva] = {
            "datetime_inicio": dados.datetime_inicio,
            "datetime_fim": dados.datetime_fim, 
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "id_sala": dados.id_sala
            }

app.include_router(router)
 
if __name__ == "__main__":
    uvicorn.run("routes:app", host="localhost", port=8000, reload=True)

#     "reserva": {
    #     "id": 1,
    #     "id_sala": 1,
    #     "semestral": boolean,
    #     "id_disciplina": 1,
    #     "datetime_inicio": "2026-04-10 08:00",
    #     "datetime_fim": "2026-04-10 10:00",
    #     "descricao": "Aula"
    # }