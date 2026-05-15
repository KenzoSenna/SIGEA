from fastapi import FastAPI, APIRouter, HTTPException
from datetime import date, time
from pydantic import BaseModel, model_validator
from typing import Union, Literal, List
import uvicorn

app = FastAPI()
router = APIRouter(tags=["Sistema de reserva"])
 
class LoginRequest(BaseModel):
    email: str
    senha: str
    #role: int

class ReservaSemestral(BaseModel):
    data_inicio: date
    data_fim: date
    horario_inicio: time
    horario_fim: time
    dias_semana: List[Literal["segunda","terca","quarta","quinta","sexta","sabado","domingo"]]

class ReservaDiaria(BaseModel):
    data: date
    horario_inicio: time
    horario_fim: time

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
    
EMAIL = "usuario@email.com"
SENHA = "senha123"
# ROLE_PROFESSOR = 0
# ROLE_ALUNO = 1
salas = [201, 202, 204]
reservas = {}
contador_reserva = 0

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
    
    contador_reserva += 1
    id_reserva = contador_reserva
    
    if dados.tipo_reserva == "diaria":
        reservas[id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data": dados.detalhes.data,
            "horario_inicio": dados.detalhes.horario_inicio,
            "horario_fim": dados.detalhes.horario_fim,
        }

        """_summary_
        o problema dessa lógica é que ele só consegue setar um horario para os dois dias
        o usuario precisa setar o horario por dia de aula

        RESOLUÇÃO (sugestão)-
            A cada dia que o usuario adicionar, adiciona um campo de horario para cada dia da semana
        Ex:
            dias_semana: ["segunda", "terca"]
            horario_inicio_segunda : ....
            horario_fim_segunda : ....
            horario_inicio_terca : ....
            horario_fim_terca : ....
        """
    elif dados.tipo_reserva == "semestral":
        reservas[id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data_inicio": dados.detalhes.data_inicio,
            "data_fim": dados.detalhes.data_fim,
            "dias_semana": dados.detalhes.dias_semana,
            "horario_inicio": dados.detalhes.horario_inicio,
            "horario_fim": dados.detalhes.horario_fim,
        }

    return {
        "sucesso": True, 
        "mensagem": f"Reserva {dados.tipo_reserva} realizada com sucesso!",
        "id_reserva": id_reserva,
        "reserva": reservas[id_reserva]
    }        
app.include_router(router)
 
if __name__ == "__main__":
    uvicorn.run("_routes:app", host="localhost", port=8000, reload=True)