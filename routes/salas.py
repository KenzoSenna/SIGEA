from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.schemas import SalaCreate, SalaResponse
from routes.store import get_current_user
from database.settings import get_db
from models import Sala, Andar, Usuario

router = APIRouter(
    tags=["Salas"]
)


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

        andar = (
            db.query(Andar)
            .filter(Andar.id_andar == dados.id_andar)
            .first()
        )

        if not andar:
            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Andar não encontrado"
                }
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
                    "mensagem": "Já existe uma sala com este nome neste andar"
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
            "sala": {
                "id_sala": nova_sala.id_sala,
                "nome": nova_sala.nome,
                "capacidade": nova_sala.capacidade,
                "tipo": nova_sala.tipo,
                "status": nova_sala.status,
                "horario_inicio": str(nova_sala.horario_inicio),
                "horario_fim": str(nova_sala.horario_fim),
                "id_andar": nova_sala.id_andar,
            }
        }

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail={
                "sucesso": False,
                "mensagem": "Erro ao criar sala - dados duplicados ou inválidos"
            }
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
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

        salas_list = [
            {
                "id_sala": s.id_sala,
                "nome": s.nome,
                "capacidade": s.capacidade,
                "tipo": s.tipo,
                "status": s.status,
                "horario_inicio": str(s.horario_inicio),
                "horario_fim": str(s.horario_fim),
                "id_andar": s.id_andar,
            }
            for s in salas
        ]

        return {
            "sucesso": True,
            "total": len(salas),
            "salas": salas_list
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
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

        sala = (
            db.query(Sala)
            .filter(Sala.id_sala == id_sala)
            .first()
        )

        if not sala:

            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Sala não encontrada"
                }
            )

        return {
            "sucesso": True,
            "sala": {
                "id_sala": sala.id_sala,
                "nome": sala.nome,
                "capacidade": sala.capacidade,
                "tipo": sala.tipo,
                "status": sala.status,
                "horario_inicio": str(sala.horario_inicio),
                "horario_fim": str(sala.horario_fim),
                "id_andar": sala.id_andar,
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
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

        sala = (
            db.query(Sala)
            .filter(Sala.id_sala == id_sala)
            .first()
        )

        if not sala:

            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Sala não encontrada"
                }
            )

        if dados.id_andar != sala.id_andar:

            andar = (
                db.query(Andar)
                .filter(Andar.id_andar == dados.id_andar)
                .first()
            )

            if not andar:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "sucesso": False,
                        "mensagem": "Andar não encontrado"
                    }
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
                    "mensagem": "Já existe uma sala com este nome neste andar"
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
            "sala": {
                "id_sala": sala.id_sala,
                "nome": sala.nome,
                "capacidade": sala.capacidade,
                "tipo": sala.tipo,
                "status": sala.status,
                "horario_inicio": str(sala.horario_inicio),
                "horario_fim": str(sala.horario_fim),
                "id_andar": sala.id_andar,
            }
        }

    except HTTPException:
        raise

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail={
                "sucesso": False,
                "mensagem": "Erro ao atualizar sala - dados duplicados ou inválidos"
            }
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
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

        sala = (
            db.query(Sala)
            .filter(Sala.id_sala == id_sala)
            .first()
        )

        if not sala:

            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Sala não encontrada"
                }
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

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
        )
