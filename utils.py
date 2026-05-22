from fastapi import HTTPException, status

ACTION_ROLES_LIST = {
	"create_reserva": ["professor", "coordenador"],
	"listar_reservas": ["professor", "coordenador"],
	"obter reserva": ["professor", "coordenador"],
	"cancelar_reserva": ["professor", "coordenador"],
	#tags de admin
	"criar_usuario": ["coordenador"],
	"listar_usuario": ["coordenador"],
	"obter_usuario": ["coordenador"],
	"deletar_usuario": ["coordenador"]
}

def validate_user_role(action: str, user_role: int) -> None:
    required_role = ACTION_ROLES_LIST.get(action, [])
    if user_role not in required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permissão insuficiente. Role necessária: {required_role}"
        )

# Dados de exemplo para andares (MOCADO)
ANDARES_MOCK = {
    1: {"id_andar": 1, "numero": 1, "descricao": "Primeiro andar"},
    2: {"id_andar": 2, "numero": 2, "descricao": "Segundo andar"},
    3: {"id_andar": 3, "numero": 3, "descricao": "Terceiro andar"},
}


def validar_andar(id_andar: int) -> bool:

    return id_andar in ANDARES_MOCK
