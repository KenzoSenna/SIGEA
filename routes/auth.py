from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routes.schemas import LoginRequest
from routes import store
from database.settings import get_db
from models import Usuario

router = APIRouter(tags=["Auth"])

@router.post("/login", summary="Fazer login")
async def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = store.get_user_by_email(dados.email, db)
    if usuario is None or not store.verify_password(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})

    access_token = store.create_access_token({
        "sub": str(usuario.id_usuario),
        "email": usuario.email,
        "tipo": usuario.tipo
    })

    return {
        "sucesso": True,
        "mensagem": "Autenticação realizada com sucesso",
        "sessao": "autenticada",
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "email": usuario.email,
            "tipo": usuario.tipo
        },
        "ativo": 1
    }


@router.post(
    "/logout",
    summary="Fazer logout"
)
async def logout(
    current_user: Usuario = Depends(store.get_current_user),
    db: Session = Depends(get_db)
):

    try:

        return {
            "sucesso": True,
            "mensagem": "Logout realizado com sucesso",
            "sessao": "finalizada",
            "usuario_id": current_user.id_usuario,
            "ativo": 0
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
        )
