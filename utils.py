from fastapi import HTTPException, status


def validate_user_role(user_role: int, required_role: int = 2) -> None:
    
    if user_role < required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permissão insuficiente. Role necessária: {required_role}"
        )

ANDARES_MOCK = {
    1: {"id_andar": 1, "numero": 1, "descricao": "Primeiro andar"},
    2: {"id_andar": 2, "numero": 2, "descricao": "Segundo andar"},
    3: {"id_andar": 3, "numero": 3, "descricao": "Terceiro andar"},
}


def validar_andar(id_andar: int) -> bool:

    return id_andar in ANDARES_MOCK
