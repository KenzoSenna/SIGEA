from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.schemas import SalaCreate, SalaResponse
from routes.store import get_current_user, tratar_integrity_error
from database.settings import get_db
from models import Sala, Andar, Usuario

router = APIRouter(
    tags=["Salas"]
)


def _serializar_sala(s: Sala) -> dict:
    return {
        "id_sala": s.id_sala,
        "nome": s.nome,
        "capacidade": s.capacidade,
        "tipo": s.tipo,
        "status": s.status,
        "horario_inicio": str(s.horario_inicio),
        "horario_fim": str(s.horario_fim),
        "id_andar": s.id_andar,
    }


@router.post(
    "/salas",
    summary="Criar nova sala",
    response_model=dict
)
async def criar_sala(
    dados: SalaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        andar = db.query(Andar).filter(Andar.id_andar == dados.id_andar).first()

        if not andar:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Andar {dados.id_andar} não encontrado"}
            )

        sala_existente = (
            db.query(Sala)
            .filter(Sala.nome == dados.nome, Sala.id_andar == dados.id_andar)
            .first()
        )

        if sala_existente:
            raise HTTPException(
                status_code=409,
                detail={
                    "sucesso": False,
                    "mensagem": f"Sala '{dados.nome}' já existe no andar {andar.numero}"
                }
            )

        nova_sala = Sala(
            nome=dados.nome,
            capacidade=dados.capacidade,
            tipo=dados.tipo,
            status=dados.status,
            horario_inicio=dados.horario_inicio,
            horario_fim=dados.horario_fim,
            id_andar=dados.id_andar,
        )

        db.add(nova_sala)
        db.commit()
        db.refresh(nova_sala)

        return {
            "sucesso": True,
            "mensagem": "Sala criada com sucesso",
            "sala": _serializar_sala(nova_sala)
        }

    except HTTPException:
        raise

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail={"sucesso": False, "mensagem": tratar_integrity_error(e)}
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.get(
    "/salas",
    summary="Listar todas as salas"
)
async def listar_salas(
    db: Session = Depends(get_db)
):

    try:

        salas = db.query(Sala).all()

        return {
            "sucesso": True,
            "total": len(salas),
            "salas": [_serializar_sala(s) for s in salas]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.get(
    "/salas/{id_sala}",
    summary="Obter detalhes de uma sala"
)
async def obter_sala(
    id_sala: int,
    db: Session = Depends(get_db)
):

    try:

        sala = db.query(Sala).filter(Sala.id_sala == id_sala).first()

        if not sala:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Sala {id_sala} não encontrada"}
            )

        return {"sucesso": True, "sala": _serializar_sala(sala)}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.put(
    "/salas/{id_sala}",
    summary="Atualizar uma sala"
)
async def atualizar_sala(
    id_sala: int,
    dados: SalaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        sala = db.query(Sala).filter(Sala.id_sala == id_sala).first()

        if not sala:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Sala {id_sala} não encontrada"}
            )

        if dados.id_andar != sala.id_andar:
            andar = db.query(Andar).filter(Andar.id_andar == dados.id_andar).first()
            if not andar:
                raise HTTPException(
                    status_code=404,
                    detail={"sucesso": False, "mensagem": f"Andar {dados.id_andar} não encontrado"}
                )

        nome_duplicado = (
            db.query(Sala)
            .filter(
                Sala.nome == dados.nome,
                Sala.id_andar == dados.id_andar,
                Sala.id_sala != id_sala
            )
            .first()
        )

        if nome_duplicado:
            raise HTTPException(
                status_code=409,
                detail={
                    "sucesso": False,
                    "mensagem": f"Sala '{dados.nome}' já existe neste andar"
                }
            )

        sala.nome = dados.nome
        sala.capacidade = dados.capacidade
        sala.tipo = dados.tipo
        sala.status = dados.status
        sala.horario_inicio = dados.horario_inicio
        sala.horario_fim = dados.horario_fim
        sala.id_andar = dados.id_andar

        db.commit()
        db.refresh(sala)

        return {
            "sucesso": True,
            "mensagem": "Sala atualizada com sucesso",
            "sala": _serializar_sala(sala)
        }

    except HTTPException:
        raise

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail={"sucesso": False, "mensagem": tratar_integrity_error(e)}
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.delete(
    "/salas/{id_sala}",
    summary="Deletar uma sala"
)
async def deletar_sala(
    id_sala: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        sala = db.query(Sala).filter(Sala.id_sala == id_sala).first()

        if not sala:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Sala {id_sala} não encontrada"}
            )

        sala_data = {
            "id_sala": sala.id_sala,
            "nome": sala.nome,
            "id_andar": sala.id_andar,
        }

        db.delete(sala)
        db.commit()

        return {
            "sucesso": True,
            "mensagem": "Sala deletada com sucesso",
            "sala_removida": sala_data
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )
