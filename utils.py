from fastapi import HTTPException, status
from routes import store


def validate_user_role(user_role: int, required_role: int = 2) -> None:
    
    if user_role < required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permissão insuficiente. Role necessária: {required_role}"
        )


def validar_andar(id_andar: int) -> bool:
    """Verifica se o andar existe no store em memória"""
    return id_andar in store.andares
