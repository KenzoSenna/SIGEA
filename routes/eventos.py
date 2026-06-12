from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.schemas import EventoCreate, UpdateEventoRequest, EventoResponse
from routes.store import (
    get_current_user,
    verificar_conflito,
    converter_para_datetime,
    tratar_integrity_error,
    obter_sala_disponivel,
    exigir_tipo,
    exigir_dono_ou_coordenador,
)
from database.settings import get_db
from models import Usuario, Evento

router = APIRouter(
    tags=["Eventos"]
)


def _serializar_evento(e: Evento) -> dict:
    return {
        "id_evento": e.id_evento,
        "nome": e.titulo,
        "descricao": e.descricao,
        "data": str(e.data_inicio.date()),
        "hora_inicio": str(e.data_inicio.time()),
        "hora_fim": str(e.data_fim.time()),
        "id_sala": e.id_sala,
        "id_usuario": e.id_usuario,
        "created_at": e.created_at.isoformat() if e.created_at else None
    }


@router.post(
    "/eventos",
    summary="Criar novo evento",
    response_model=dict
)
async def criar_evento(
    dados: EventoCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    exigir_tipo(current_user, "professor", "coordenador")

    try:

        obter_sala_disponivel(dados.id_sala, db)

        data_inicio = converter_para_datetime(dados.data, dados.hora_inicio)
        data_fim = converter_para_datetime(dados.data, dados.hora_fim)

        if verificar_conflito(id_sala=dados.id_sala, data_inicio=data_inicio, data_fim=data_fim, db=db):
            raise HTTPException(
                status_code=409,
                detail={"sucesso": False, "mensagem": f"Sala {dados.id_sala} já está ocupada neste horário"}
            )

        novo_evento = Evento(
            titulo=dados.nome,
            descricao=dados.descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            id_sala=dados.id_sala,
            id_usuario=current_user.id_usuario
        )

        db.add(novo_evento)
        db.commit()
        db.refresh(novo_evento)

        return {
            "sucesso": True,
            "mensagem": "Evento criado com sucesso",
            "id_evento": novo_evento.id_evento,
            "evento": _serializar_evento(novo_evento)
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
    "/eventos",
    summary="Listar todos os eventos"
)
async def listar_eventos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    id_sala: int | None = Query(None, description="Filtrar por sala"),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        query = db.query(Evento)
        if id_sala is not None:
            query = query.filter(Evento.id_sala == id_sala)

        total = query.count()
        eventos = query.order_by(Evento.data_inicio).offset(skip).limit(limit).all()

        return {
            "sucesso": True,
            "total": total,
            "eventos": [_serializar_evento(e) for e in eventos]
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.get(
    "/eventos/{id_evento}",
    summary="Obter detalhes de um evento"
)
async def obter_evento(
    id_evento: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        evento = db.query(Evento).filter(Evento.id_evento == id_evento).first()

        if not evento:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Evento {id_evento} não encontrado"}
            )

        return {"sucesso": True, "evento": _serializar_evento(evento)}

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.put(
    "/eventos/{id_evento}",
    summary="Atualizar um evento"
)
async def atualizar_evento(
    id_evento: int,
    dados: UpdateEventoRequest,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        evento = db.query(Evento).filter(Evento.id_evento == id_evento).first()

        if not evento:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Evento {id_evento} não encontrado"}
            )

        exigir_dono_ou_coordenador(current_user, evento.id_usuario, "alterar este evento")

        if dados.id_sala and dados.id_sala != evento.id_sala:
            obter_sala_disponivel(dados.id_sala, db)

        data_inicio = evento.data_inicio
        data_fim = evento.data_fim

        if dados.data:
            hora_i = dados.hora_inicio or evento.data_inicio.time()
            hora_f = dados.hora_fim or evento.data_fim.time()
            data_inicio = converter_para_datetime(dados.data, hora_i)
            data_fim = converter_para_datetime(dados.data, hora_f)
        elif dados.hora_inicio or dados.hora_fim:
            hora_i = dados.hora_inicio or evento.data_inicio.time()
            hora_f = dados.hora_fim or evento.data_fim.time()
            data_inicio = converter_para_datetime(evento.data_inicio.date(), hora_i)
            data_fim = converter_para_datetime(evento.data_fim.date(), hora_f)

        if data_inicio >= data_fim:
            raise HTTPException(
                status_code=422,
                detail={"sucesso": False, "mensagem": "hora_fim deve ser maior que hora_inicio"}
            )

        id_sala = dados.id_sala or evento.id_sala

        if verificar_conflito(
            id_sala=id_sala,
            data_inicio=data_inicio,
            data_fim=data_fim,
            db=db,
            exclude_id=id_evento,
            exclude_tipo="evento"
        ):
            raise HTTPException(
                status_code=409,
                detail={"sucesso": False, "mensagem": f"Sala {id_sala} já está ocupada neste horário"}
            )

        evento.titulo = dados.nome or evento.titulo
        evento.descricao = dados.descricao if dados.descricao is not None else evento.descricao
        evento.data_inicio = data_inicio
        evento.data_fim = data_fim
        evento.id_sala = id_sala

        db.commit()
        db.refresh(evento)

        return {
            "sucesso": True,
            "mensagem": "Evento atualizado com sucesso",
            "evento": _serializar_evento(evento)
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )


@router.delete(
    "/eventos/{id_evento}",
    summary="Deletar um evento"
)
async def deletar_evento(
    id_evento: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        evento = db.query(Evento).filter(Evento.id_evento == id_evento).first()

        if not evento:
            raise HTTPException(
                status_code=404,
                detail={"sucesso": False, "mensagem": f"Evento {id_evento} não encontrado"}
            )

        exigir_dono_ou_coordenador(current_user, evento.id_usuario, "excluir este evento")

        evento_data = {
            "id_evento": evento.id_evento,
            "nome": evento.titulo,
            "id_sala": evento.id_sala
        }

        db.delete(evento)
        db.commit()

        return {
            "sucesso": True,
            "mensagem": "Evento deletado com sucesso",
            "evento_removido": evento_data
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"sucesso": False, "mensagem": "Erro interno do servidor"}
        )
