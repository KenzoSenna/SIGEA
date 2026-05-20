from fastapi import APIRouter, HTTPException
from routes.schemas import LoginRequest
from routes import store

router = APIRouter(tags=["Auth"])

@router.post("/login", summary="Fazer login")
async def login(dados: LoginRequest):
    usuario = store.get_user_by_email(dados.email)
    if usuario is None or not store.verify_password(dados.senha, usuario["senha_hash"]):
        raise HTTPException(status_code=401, detail={"sucesso": False, "mensagem": "Credenciais inválidas"})

    access_token = store.create_access_token({
        "sub": str(usuario["id_usuario"]),
        "email": usuario["email"],
        "tipo": usuario["tipo"]
    })

    return {
        "sucesso": True,
        "mensagem": "Autenticação realizada com sucesso",
        "sessao": "autenticada",
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id_usuario": usuario["id_usuario"],
            "email": usuario["email"],
            "tipo": usuario["tipo"]
        }
    }
