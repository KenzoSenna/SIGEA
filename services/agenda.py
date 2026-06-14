from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Evento, Reserva, Sala, StatusSala


def verificar_conflito(
    id_sala: int,
    data_inicio: datetime,
    data_fim: datetime,
    db: Session,
    exclude_id: int | None = None,
    exclude_tipo: str = "reserva",
) -> bool:
    
    reservas = db.query(Reserva.id_reserva).filter(
        Reserva.id_sala == id_sala,
        Reserva.data_inicio < data_fim,
        Reserva.data_fim > data_inicio,
    )
    if exclude_tipo == "reserva" and exclude_id is not None:
        reservas = reservas.filter(Reserva.id_reserva != exclude_id)

    if reservas.first() is not None:
        return True

    eventos = db.query(Evento.id_evento).filter(
        Evento.id_sala == id_sala,
        Evento.data_inicio < data_fim,
        Evento.data_fim > data_inicio,
    )
    if exclude_tipo == "evento" and exclude_id is not None:
        eventos = eventos.filter(Evento.id_evento != exclude_id)

    return eventos.first() is not None


def obter_sala_disponivel(id_sala: int, db: Session) -> Sala:
    
    sala = db.query(Sala).filter(Sala.id_sala == id_sala).first()

    if not sala:
        raise HTTPException(
            status_code=404,
            detail={"sucesso": False, "mensagem": f"Sala {id_sala} não encontrada"},
        )

    if sala.status != StatusSala.ATIVA:
        raise HTTPException(
            status_code=409,
            detail={
                "sucesso": False,
                "mensagem": f"Sala {id_sala} não está disponível (status: {sala.status.value})",
            },
        )

    return sala
