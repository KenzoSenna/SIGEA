from fastapi import APIRouter, HTTPException, status, Header
from models.andar import AndarCreate
from routes import store
from utils import validate_user_role

router = APIRouter(tags=["Andares"])

@router.post("/andares", summary="Cadastrar um novo andar", status_code=status.HTTP_201_CREATED)
async def cadastrar_andar(
    dados: AndarCreate,
    user_role: int = Header(..., description="Role do usuário (Requer nível 3: Admin)")
):
    # Validar permissão do usuário
    validate_user_role(user_role, required_role=3)

    # Validar se já existe um andar com o MESMO nome no MESMO bloco
    for andar in store.andares.values():
        if andar["nome"].lower() == dados.nome.value.lower() and andar["bloco"].lower() == dados.bloco.value.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"sucesso": False, "mensagem": f"O {dados.nome.value} já está cadastrado no {dados.bloco.value}."}
            )
    
    # Salvar em store.py
    store.contador_andar += 1
    id_andar = store.contador_andar
    
    novo_andar = {
        "id_andar": id_andar,
        "nome": dados.nome.value,
        "bloco": dados.bloco.value
    }
    
    store.andares[id_andar] = novo_andar
    
    return {
        "sucesso": True,
        "mensagem": "Andar criado com sucesso",
        "andar": novo_andar
    }

@router.get("/andares", summary="Listar todos os andares")
async def listar_andares():
    lista_andares = list(store.andares.values())
    return {
        "sucesso": True,
        "total": len(store.andares),
        "andares": lista_andares
    }
