from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.schemas import CriarAndarRequest, AtualizarAndarRequest, AndarResponse
from routes.store import get_current_user
from database.settings import get_db
from models import Andar, Sala, Usuario

router = APIRouter(
    tags=["Andares"]
)


@router.post(
    "/andares",
    summary="Criar novo andar",
    response_model=dict
)
async def criar_andar(
    dados: CriarAndarRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        andar_existente = (
            db.query(Andar)
            .filter(Andar.numero == dados.numero)
            .first()
        )

        if andar_existente:
            raise HTTPException(
                status_code=409,
                detail={
                    "sucesso": False,
                    "mensagem": "Andar com este número já existe"
                }
            )

        novo_andar = Andar(
            numero=dados.numero,
            pos_x=dados.pos_x,
            pos_y=dados.pos_y
        )

        db.add(novo_andar)

        db.commit()

        db.refresh(novo_andar)

        return {
            "sucesso": True,
            "mensagem": "Andar criado com sucesso",
            "id_andar": novo_andar.id_andar,
            "andar": {
                "id_andar": novo_andar.id_andar,
                "numero": novo_andar.numero,
                "pos_x": novo_andar.pos_x,
                "pos_y": novo_andar.pos_y
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
                "mensagem": "Erro ao criar andar - dados duplicados ou inválidos"
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
    "/andares",
    summary="Listar todos os andares"
)
async def listar_andares(
    db: Session = Depends(get_db)
):

    try:

        andares = db.query(Andar).all()

        andares_list = []

        for a in andares:

            andares_list.append({
                "id_andar": a.id_andar,
                "numero": a.numero,
                "pos_x": a.pos_x,
                "pos_y": a.pos_y
            })

        return {
            "sucesso": True,
            "total": len(andares),
            "andares": andares_list
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
    "/andares/{id_andar}",
    summary="Obter detalhes de um andar"
)
async def obter_andar(
    id_andar: int,
    db: Session = Depends(get_db)
):

    try:

        andar = (
            db.query(Andar)
            .filter(Andar.id_andar == id_andar)
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

        salas = (
            db.query(Sala)
            .filter(Sala.id_andar == id_andar)
            .all()
        )

        salas_list = [
            {
                "id_sala": s.id_sala,
                "nome": s.nome,
                "capacidade": s.capacidade
            }
            for s in salas
        ]

        return {
            "sucesso": True,
            "andar": {
                "id_andar": andar.id_andar,
                "numero": andar.numero,
                "pos_x": andar.pos_x,
                "pos_y": andar.pos_y,
                "total_salas": len(salas),
                "salas": salas_list
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
    "/andares/{id_andar}",
    summary="Atualizar um andar"
)
async def atualizar_andar(
    id_andar: int,
    dados: AtualizarAndarRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        andar = (
            db.query(Andar)
            .filter(Andar.id_andar == id_andar)
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

        if dados.numero is not None and dados.numero != andar.numero:

            andar_existente = (
                db.query(Andar)
                .filter(Andar.numero == dados.numero)
                .first()
            )

            if andar_existente:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "sucesso": False,
                        "mensagem": "Já existe um andar com este número"
                    }
                )

        andar.numero = dados.numero if dados.numero is not None else andar.numero
        andar.pos_x = dados.pos_x if dados.pos_x is not None else andar.pos_x
        andar.pos_y = dados.pos_y if dados.pos_y is not None else andar.pos_y

        db.commit()

        db.refresh(andar)

        return {
            "sucesso": True,
            "mensagem": "Andar atualizado com sucesso",
            "andar": {
                "id_andar": andar.id_andar,
                "numero": andar.numero,
                "pos_x": andar.pos_x,
                "pos_y": andar.pos_y
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
                "mensagem": "Erro ao atualizar andar - dados duplicados"
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
    "/andares/{id_andar}",
    summary="Deletar um andar"
)
async def deletar_andar(
    id_andar: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        andar = (
            db.query(Andar)
            .filter(Andar.id_andar == id_andar)
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

        salas = (
            db.query(Sala)
            .filter(Sala.id_andar == id_andar)
            .all()
        )

        if salas:

            raise HTTPException(
                status_code=409,
                detail={
                    "sucesso": False,
                    "mensagem": f"Não é possível deletar este andar. Existem {len(salas)} sala(s) associada(s)"
                }
            )

        andar_data = {
            "id_andar": andar.id_andar,
            "numero": andar.numero
        }

        db.delete(andar)

        db.commit()

        return {
            "sucesso": True,
            "mensagem": "Andar deletado com sucesso",
            "andar_removido": andar_data
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
