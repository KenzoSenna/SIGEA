from fastapi import APIRouter, HTTPException
from routes.schemas import CriarUsuarioRequest
from routes import store

router = APIRouter(tags=["Usuários"])

@router.post("/usuarios", summary="Criar novo usuário")
async def criar_usuario(dados: CriarUsuarioRequest):
    if dados.email in store.emails_cadastrados:
        raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Email já cadastrado"})
    
    store.contador_usuario += 1
    id_usuario = store.contador_usuario
    
    store.usuarios[id_usuario] = {
        "id_usuario": id_usuario,
        "nome": dados.nome,
        "email": dados.email,
        "senha_hash": store.get_password_hash(dados.senha),
        "tipo": dados.tipo,
        "created_at": str(__import__('datetime').datetime.now().isoformat())
    }
    
    store.emails_cadastrados.add(dados.email)
    
    return {
        "sucesso": True,
        "mensagem": "Usuário criado com sucesso",
        "id_usuario": id_usuario,
        "usuario": {
            "id_usuario": store.usuarios[id_usuario]["id_usuario"],
            "nome": store.usuarios[id_usuario]["nome"],
            "email": store.usuarios[id_usuario]["email"],
            "tipo": store.usuarios[id_usuario]["tipo"],
            "created_at": store.usuarios[id_usuario]["created_at"]
        }
    }

@router.get("/usuarios", summary="Listar todos os usuários")
async def listar_usuarios():
    lista_usuarios = []
    for usuario in store.usuarios.values():
        lista_usuarios.append({
            "id_usuario": usuario["id_usuario"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "tipo": usuario["tipo"],
            "created_at": usuario["created_at"]
        })
    
    return {
        "sucesso": True,
        "total": len(store.usuarios),
        "usuarios": lista_usuarios
    }

@router.get("/usuarios/{id_usuario}", summary="Obter detalhes de um usuário")
async def obter_usuario(id_usuario: int):
    if id_usuario not in store.usuarios:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})
    
    usuario = store.usuarios[id_usuario]
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

@router.delete("/usuarios/{id_usuario}", summary="Deletar um usuário")
async def deletar_usuario(id_usuario: int):
    if id_usuario not in store.usuarios:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})
    
    usuario_removido = store.usuarios.pop(id_usuario)
    store.emails_cadastrados.discard(usuario_removido["email"])
    
    return {
        "sucesso": True,
        "mensagem": "Usuário deletado com sucesso",
        "usuario_removido": {
            "id_usuario": usuario_removido["id_usuario"],
            "nome": usuario_removido["nome"],
            "email": usuario_removido["email"]
        }
    }
