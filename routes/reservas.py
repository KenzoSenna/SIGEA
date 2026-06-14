from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schemas import ReservaRequest
from dependencies.auth import get_current_user
from services.agenda import verificar_conflito, obter_sala_disponivel
from services.authorization import exigir_dono_ou_coordenador
from database.settings import get_db
from models import Usuario, Reserva

router = APIRouter(
    tags=["Reservas"]
)


def _serializar_reserva(r: Reserva) -> dict:
    return {
        "id_reserva": r.id_reserva,
        "id_sala": r.id_sala,
        "id_usuario": r.id_usuario,
        "id_disciplina": r.id_disciplina,
        "descricao": r.descricao,
        "status": r.status,
        "data_inicio": str(r.data_inicio),
        "data_fim": str(r.data_fim),
        "created_at": str(r.created_at),
    }


@router.post(
    "/reservas",
    summary="Realizar reserva de sala",
    response_model=dict
)
async def create_reserva(
    dados: ReservaRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        obter_sala_disponivel(dados.id_sala, db)

        if verificar_conflito(
            id_sala=dados.id_sala,
            data_inicio=dados.data_inicio,
            data_fim=dados.data_fim,
            db=db
        ):
            raise HTTPException(
                status_code=409,
                detail={"sucesso": False, "mensagem": f"Sala {dados.id_sala} já está ocupada neste horário"}
            )

        reserva = Reserva(
            id_sala=dados.id_sala,
            id_disciplina=dados.id_disciplina,
            id_usuario=current_user.id_usuario,
            descricao=dados.descricao,
            data_inicio=dados.data_inicio,
            data_fim=dados.data_fim,
        )

        db.add(reserva)
        db.commit()
        db.refresh(reserva)

        return {
            "sucesso": True,
            "mensagem": "Reserva realizada com sucesso",
            "id_reserva": reserva.id_reserva,
            "reserva": _serializar_reserva(reserva)
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.get(
    "/reservas",
    summary="Listar todas as reservas"
)
async def listar_reservas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    id_sala: int | None = Query(None, description="Filtrar por sala"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        query = db.query(Reserva)
        if id_sala is not None:
            query = query.filter(Reserva.id_sala == id_sala)

        total = query.count()
        reservas = query.order_by(Reserva.data_inicio).offset(skip).limit(limit).all()

        return {
            "sucesso": True,
            "total": total,
            "reservas": [_serializar_reserva(r) for r in reservas]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.get(
    "/reservas/{id_reserva}",
    summary="Obter detalhes de uma reserva"
)
async def obter_reserva(
    id_reserva: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

        if not reserva:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Reserva {id_reserva} não encontrada"}
            )

        return {"sucesso": True, "reserva": _serializar_reserva(reserva)}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.delete(
    "/reservas/{id_reserva}",
    summary="Cancelar uma reserva"
)
async def cancelar_reserva(
    id_reserva: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

        if not reserva:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Reserva {id_reserva} não encontrada"}
            )

        exigir_dono_ou_coordenador(current_user, reserva.id_usuario, "cancelar esta reserva")

        reserva_data = {
            "id_reserva": reserva.id_reserva,
            "id_sala": reserva.id_sala,
            "status": reserva.status,
        }

        db.delete(reserva)
        db.commit()

        return {
            "sucesso": True,
            "mensagem": "Reserva cancelada com sucesso",
            "reserva_removida": reserva_data
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )
