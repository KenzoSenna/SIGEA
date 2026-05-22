from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.schemas import ReservaRequest, ReservaResponse
from routes import store
from database.settings import get_db
from models import Usuario, Reserva, TipoReserva, Sala
from datetime import date
import json

router = APIRouter(tags=["Reservas"])

@router.post("/reservas", summary="Realizar reserva de sala", response_model=dict)
async def create_reserva(
    dados: ReservaRequest, 
    current_user: Usuario = Depends(store.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Verificar se sala existe
        sala = db.query(Sala).filter(Sala.id_sala == dados.id_sala).first()
        if not sala:
            raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Sala não encontrada"})
        
        # Verificar conflito de horários
        if store.verificar_conflito(dados.id_sala, dados.detalhes, dados.tipo_reserva, db):
            raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Horário indisponível nesta sala"})
        
        # Criar reserva no banco
        if dados.tipo_reserva == "diaria":
            reserva = Reserva(
                id_sala=dados.id_sala,
                id_disciplina=dados.id_disciplina,
                id_usuario=current_user.id_usuario,
                descricao=dados.descricao,
                tipo_reserva=TipoReserva.DIARIA,
                data=dados.detalhes.data,
                horario_inicio=dados.detalhes.horario_inicio,
                horario_fim=dados.detalhes.horario_fim,
            )
        elif dados.tipo_reserva == "semestral":
            reserva = Reserva(
                id_sala=dados.id_sala,
                id_disciplina=dados.id_disciplina,
                id_usuario=current_user.id_usuario,
                descricao=dados.descricao,
                tipo_reserva=TipoReserva.SEMESTRAL,
                data_inicio=dados.detalhes.data_inicio,
                data_fim=dados.detalhes.data_fim,
                dias_semana=dados.detalhes.dias_semana,
                horarios={dia: {"inicio": str(h["inicio"]), "fim": str(h["fim"])} 
                         for dia, h in dados.detalhes.horarios.items()},
            )
        
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        
        return {
            "sucesso": True,
            "mensagem": f"Reserva {dados.tipo_reserva} realizada com sucesso!",
            "id_reserva": reserva.id_reserva,
            "reserva": {
                "id_reserva": reserva.id_reserva,
                "id_sala": reserva.id_sala,
                "id_usuario": reserva.id_usuario,
                "tipo_reserva": reserva.tipo_reserva,
                "data": str(reserva.data) if reserva.data else None,
                "horario_inicio": str(reserva.horario_inicio) if reserva.horario_inicio else None,
                "horario_fim": str(reserva.horario_fim) if reserva.horario_fim else None,
                "data_inicio": str(reserva.data_inicio) if reserva.data_inicio else None,
                "data_fim": str(reserva.data_fim) if reserva.data_fim else None,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})


@router.get("/reservas", summary="Listar todas as reservas")
async def listar_reservas(
    current_user: Usuario = Depends(store.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        reservas = db.query(Reserva).all()
        reservas_list = []
        for r in reservas:
            reservas_list.append({
                "id_reserva": r.id_reserva,
                "id_sala": r.id_sala,
                "id_usuario": r.id_usuario,
                "descricao": r.descricao,
                "tipo_reserva": r.tipo_reserva,
                "data": str(r.data) if r.data else None,
                "horario_inicio": str(r.horario_inicio) if r.horario_inicio else None,
                "horario_fim": str(r.horario_fim) if r.horario_fim else None,
                "data_inicio": str(r.data_inicio) if r.data_inicio else None,
                "data_fim": str(r.data_fim) if r.data_fim else None,
            })
        return {
            "sucesso": True,
            "total": len(reservas),
            "reservas": reservas_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})


@router.get("/reservas/{id_reserva}", summary="Obter detalhes de uma reserva")
async def obter_reserva(
    id_reserva: int,
    current_user: Usuario = Depends(store.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Reserva não encontrada"})
        
        return {
            "sucesso": True,
            "reserva": {
                "id_reserva": reserva.id_reserva,
                "id_sala": reserva.id_sala,
                "id_usuario": reserva.id_usuario,
                "descricao": reserva.descricao,
                "tipo_reserva": reserva.tipo_reserva,
                "data": str(reserva.data) if reserva.data else None,
                "horario_inicio": str(reserva.horario_inicio) if reserva.horario_inicio else None,
                "horario_fim": str(reserva.horario_fim) if reserva.horario_fim else None,
                "data_inicio": str(reserva.data_inicio) if reserva.data_inicio else None,
                "data_fim": str(reserva.data_fim) if reserva.data_fim else None,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})


@router.delete("/reservas/{id_reserva}", summary="Cancelar uma reserva")
async def cancelar_reserva(
    id_reserva: int,
    current_user: Usuario = Depends(store.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Reserva não encontrada"})
        
        reserva_data = {
            "id_reserva": reserva.id_reserva,
            "id_sala": reserva.id_sala,
            "tipo_reserva": reserva.tipo_reserva,
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail={"sucesso": False, "mensagem": str(e)})
