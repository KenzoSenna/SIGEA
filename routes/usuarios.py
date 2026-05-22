from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.schemas import CriarUsuarioRequest, UsuarioResponse
from routes import store
from database.settings import get_db
from models import Usuario, TipoUsuario

router = APIRouter(tags=["Usuários"])

@router.post("/usuarios", summary="Criar novo usuário", response_model=dict)
async def criar_usuario(dados: CriarUsuarioRequest, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == dados.email.lower()).first()
    if usuario_existente:
        raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Email já cadastrado"})
    
    try:
        novo_usuario = Usuario(
            nome=dados.nome,
            email=dados.email.lower(),
            senha_hash=store.get_password_hash(dados.senha),
            tipo=dados.tipo,
        )
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        
        return {
            "sucesso": True,
            "mensagem": "Usuário criado com sucesso",
            "id_usuario": novo_usuario.id_usuario,
            "usuario": {
                "id_usuario": novo_usuario.id_usuario,
                "nome": novo_usuario.nome,
                "email": novo_usuario.email,
                "tipo": novo_usuario.tipo,
                "created_at": novo_usuario.created_at.isoformat()
            }
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Erro ao criar usuário"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})


@router.get("/usuarios", summary="Listar todos os usuários")
async def listar_usuarios(db: Session = Depends(get_db)):
    try:
        usuarios = db.query(Usuario).all()
        lista_usuarios = [
            {
                "id_usuario": u.id_usuario,
                "nome": u.nome,
                "email": u.email,
                "tipo": u.tipo,
                "created_at": u.created_at.isoformat() if u.created_at else None
            }
            for u in usuarios
        ]
        return {
            "sucesso": True,
            "total": len(usuarios),
            "usuarios": lista_usuarios
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})


@router.get("/usuarios/{id_usuario}", summary="Obter detalhes de um usuário")
async def obter_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})
        
        return {
            "sucesso": True,
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nome": usuario.nome,
                "email": usuario.email,
                "tipo": usuario.tipo,
                "created_at": usuario.created_at.isoformat() if usuario.created_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})


@router.delete("/usuarios/{id_usuario}", summary="Deletar um usuário")
async def deletar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    try:
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})
        
        usuario_data = {
            "id_usuario": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email
        }
        
        db.delete(usuario)
        db.commit()
        
        return {
            "sucesso": True,
            "mensagem": "Usuário deletado com sucesso",
            "usuario_removido": usuario_data
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})
