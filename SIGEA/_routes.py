from fastapi import FastAPI, APIRouter, HTTPException
from datetime import date, time
from pydantic import BaseModel, model_validator
from typing import Union, Literal
import uvicorn

app = FastAPI()
router = APIRouter(prefix="/auth", tags=["Autenticação"])
 
class LoginRequest(BaseModel):
    email: str
    senha: str
    #role: int

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
    id_disciplina: int
    descricao: str
    tipo_reserva: Literal["diaria", "semestral"]  # Garante apenas estas duas opções
    detalhes: Union[ReservaDiaria, ReservaSemestral]  # Aceita um modelo ou o outro

    def verificar_tipo_detalhes(self):
        if self.tipo_reserva == "diaria" and not isinstance(self.detalhes, ReservaDiaria):
            raise ValueError("Para 'tipo_reserva' igual a 'diaria', insira os campos de ReservaDiaria.")
        if self.tipo_reserva == "semestral" and not isinstance(self.detalhes, ReservaSemestral):
            raise ValueError("Para 'tipo_reserva' igual a 'semestral', insira os campos de ReservaSemestral.")
        return self
    
EMAIL = "usuario@email.com"
SENHA = "senha123"
# ROLE_PROFESSOR = 0
# ROLE_ALUNO = 1
salas = [201, 202, 204]
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
    if dados.id_sala not in salas:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Sala não encontrada"}) 
    if dados.tipo_reserva == "diaria":
        reservas[dados.id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data": dados.detalhes.data,
            "horario_inicio": dados.detalhes.horario_inicio,
            "horario_fim": dados.detalhes.horario_fim,
        }

    elif dados.tipo_reserva == "semestral":
        reservas[dados.id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data_inicio": dados.detalhes.data_inicio,
            "data_fim": dados.detalhes.data_fim,
            "horario_inicio": dados.detalhes.horario_inicio,
            "horario_fim": dados.detalhes.horario_fim,
        }

    return {
        "sucesso": True, 
        "mensagem": f"Reserva {dados.tipo_reserva} realizada com sucesso!",
        "dados_salvos": reservas[dados.id_reserva]
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