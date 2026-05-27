from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from routes.schemas import EventoCreate, UpdateEventoRequest, EventoResponse
from routes.store import get_current_user, verificar_conflito, converter_para_datetime
from database.settings import get_db
from models import Usuario, Evento, Sala

router = APIRouter(
    tags=["Eventos"]
)


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

    try:

        sala = (
            db.query(Sala)
            .filter(Sala.id_sala == dados.id_sala)
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

        data_inicio = converter_para_datetime(dados.data, dados.hora_inicio)
        data_fim = converter_para_datetime(dados.data, dados.hora_fim)

        conflito = verificar_conflito(
            id_sala=dados.id_sala,
            data_inicio=data_inicio,
            data_fim=data_fim,
            db=db
        )

        if conflito:
            raise HTTPException(
                status_code=409,
                detail={
                    "sucesso": False,
                    "mensagem": "Horário indisponível nesta sala"
                }
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
            "evento": {
                "id_evento": novo_evento.id_evento,
                "nome": novo_evento.titulo,
                "descricao": novo_evento.descricao,
                "data": str(novo_evento.data_inicio.date()),
                "hora_inicio": str(novo_evento.data_inicio.time()),
                "hora_fim": str(novo_evento.data_fim.time()),
                "id_sala": novo_evento.id_sala,
                "id_usuario": novo_evento.id_usuario,
                "created_at": novo_evento.created_at.isoformat() if novo_evento.created_at else None
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
                "mensagem": "Erro ao criar evento - dados duplicados ou inválidos"
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
    "/eventos",
    summary="Listar todos os eventos"
)
async def listar_eventos(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        eventos = db.query(Evento).all()

        eventos_list = []

        for e in eventos:

            eventos_list.append({
                "id_evento": e.id_evento,
                "nome": e.titulo,
                "descricao": e.descricao,
                "data": str(e.data_inicio.date()),
                "hora_inicio": str(e.data_inicio.time()),
                "hora_fim": str(e.data_fim.time()),
                "id_sala": e.id_sala,
                "id_usuario": e.id_usuario,
                "created_at": e.created_at.isoformat() if e.created_at else None
            })

        return {
            "sucesso": True,
            "total": len(eventos),
            "eventos": eventos_list
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
    "/eventos/{id_evento}",
    summary="Obter detalhes de um evento"
)
async def obter_evento(
    id_evento: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:

        evento = (
            db.query(Evento)
            .filter(Evento.id_evento == id_evento)
            .first()
        )

        if not evento:

            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Evento não encontrado"
                }
            )

        return {
            "sucesso": True,
            "evento": {
                "id_evento": evento.id_evento,
                "nome": evento.titulo,
                "descricao": evento.descricao,
                "data": str(evento.data_inicio.date()),
                "hora_inicio": str(evento.data_inicio.time()),
                "hora_fim": str(evento.data_fim.time()),
                "id_sala": evento.id_sala,
                "id_usuario": evento.id_usuario,
                "created_at": evento.created_at.isoformat() if evento.created_at else None
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

        evento = (
            db.query(Evento)
            .filter(Evento.id_evento == id_evento)
            .first()
        )

        if not evento:

            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Evento não encontrado"
                }
            )

        if dados.id_sala and dados.id_sala != evento.id_sala:

            sala = (
                db.query(Sala)
                .filter(Sala.id_sala == dados.id_sala)
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

        data_inicio = evento.data_inicio
        data_fim = evento.data_fim

        if dados.data:
            if dados.hora_inicio:
                data_inicio = converter_para_datetime(dados.data, dados.hora_inicio)
            else:
                data_inicio = converter_para_datetime(dados.data, evento.data_inicio.time())

            if dados.hora_fim:
                data_fim = converter_para_datetime(dados.data, dados.hora_fim)
            else:
                data_fim = converter_para_datetime(dados.data, evento.data_fim.time())

        elif dados.hora_inicio or dados.hora_fim:

            hora_inicio = dados.hora_inicio or evento.data_inicio.time()
            hora_fim = dados.hora_fim or evento.data_fim.time()

            data_inicio = converter_para_datetime(evento.data_inicio.date(), hora_inicio)
            data_fim = converter_para_datetime(evento.data_fim.date(), hora_fim)

        id_sala = dados.id_sala or evento.id_sala

        conflito = verificar_conflito(
            id_sala=id_sala,
            data_inicio=data_inicio,
            data_fim=data_fim,
            db=db,
            exclude_id=id_evento,
            exclude_tipo="evento"
        )

        if conflito:
            raise HTTPException(
                status_code=409,
                detail={
                    "sucesso": False,
                    "mensagem": "Horário indisponível nesta sala"
                }
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
            "evento": {
                "id_evento": evento.id_evento,
                "nome": evento.titulo,
                "descricao": evento.descricao,
                "data": str(evento.data_inicio.date()),
                "hora_inicio": str(evento.data_inicio.time()),
                "hora_fim": str(evento.data_fim.time()),
                "id_sala": evento.id_sala,
                "id_usuario": evento.id_usuario,
                "created_at": evento.created_at.isoformat() if evento.created_at else None
            }
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

        evento = (
            db.query(Evento)
            .filter(Evento.id_evento == id_evento)
            .first()
        )

        if not evento:

            raise HTTPException(
                status_code=404,
                detail={
                    "sucesso": False,
                    "mensagem": "Evento não encontrado"
                }
            )

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

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail={
                "sucesso": False,
                "mensagem": str(e)
            }
        )
