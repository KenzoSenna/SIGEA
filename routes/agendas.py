from fastapi import APIRouter, HTTPException, Query, Depends, Header
from collections import defaultdict
from routes import store
from typing import Optional
router = APIRouter(tags=["Agendas"])

@router.get("/agendas/usuario/{id_usuario}", summary="Visualizar agenda do usuário")
async def agenda_usuario(
    id_usuario: int,
    usuario_logado: dict = Depends(store.get_current_user),
    user_role: int = Header(1, description="Nível de acesso (1=Aluno, 3=Admin)")
):
    if id_usuario not in store.usuarios:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Usuário não encontrado"})

    # Só pode ver a própria agenda, a não ser que seja Admin (Nível 3)
    if usuario_logado["id_usuario"] != id_usuario and user_role < 3:
        raise HTTPException(status_code=403, detail={"sucesso": False, "mensagem": "Acesso negado. Você só pode visualizar a sua própria agenda."})
    
    itens_agenda = []

    # Buscar reservas do usuário (Caso o usuario seja o role de professor)
    for reserva in store.reservas.values():
        if reserva.get("id_usuario") == id_usuario:
            itens_agenda.append({
                "tipo": "reserva",
                "id": reserva.get("id_reserva"),
                "data": reserva.get("data"),
                "horario_inicio": reserva.get("horario_inicio"),
                "horario_fim": reserva.get("horario_fim"),
                "descricao": reserva.get("descricao"),
                "local": f"Sala {reserva.get('id_sala')}"
            })

    # Buscar eventos onde o usuário está inscrito (Caso o usuário seja o role de aluno)
    for evento in store.eventos.values():
        inscrito = any(
            inscricao.get("id_usuario") == id_usuario and inscricao.get("id_evento") == evento.get("id_evento")
            for inscricao in store.inscricoes_eventos
        )
        if inscrito:
            itens_agenda.append({
                "tipo": "evento",
                "id": evento.get("id_evento"),
                "data": evento.get("data"),
                "horario_inicio": evento.get("horario_inicio"),
                "horario_fim": evento.get("horario_fim"),
                "titulo": evento.get("titulo"),
                "ministrante": evento.get("ministrante"),
                "local": f"Sala {evento.get('id_sala')}"
            })

    # Organizar resultados por data
    agenda_organizada = defaultdict(list)
    for item in itens_agenda:
        data_item = item.get("data")
        agenda_organizada[data_item].append(item)

    # Opcional: ordenar horários dentro de cada data
    for data in agenda_organizada:
        agenda_organizada[data].sort(key=lambda x: x.get("horario_inicio", ""))

    return {
        "sucesso": True,
        "id_usuario": id_usuario,
        "agenda": dict(agenda_organizada)
    }

@router.get("/agendas/geral", summary="Visualizar agenda geral (Filtro por mês ou tudo)")
async def agenda_geral(mes_ano: Optional[str] = Query(None, description="Mês/Ano no formato YYYY-MM. Se vazio, retorna tudo.")):
    itens_filtrados = []

    # Buscar reservas filtradas (Caso o usuario seja o role de professor)
    for reserva in store.reservas.values():
        data_reserva = reserva.get("data", "")
        if not mes_ano or data_reserva.startswith(mes_ano):
            itens_filtrados.append({
                "tipo": "reserva",
                "id": reserva.get("id_reserva"),
                "data": data_reserva,
                "horario_inicio": reserva.get("horario_inicio"),
                "horario_fim": reserva.get("horario_fim"),
                "descricao": reserva.get("descricao"),
                "id_usuario": reserva.get("id_usuario"),
                "local": f"Sala {reserva.get('id_sala')}"
            })

    # Buscar eventos filtrados (Caso o usuario seja o role de aluno)
    for evento in store.eventos.values():
        data_evento = evento.get("data", "")
        if not mes_ano or data_evento.startswith(mes_ano):
            itens_filtrados.append({
                "tipo": "evento",
                "id": evento.get("id_evento"),
                "data": data_evento,
                "horario_inicio": evento.get("horario_inicio"),
                "horario_fim": evento.get("horario_fim"),
                "titulo": evento.get("titulo"),
                "ministrante": evento.get("ministrante"),
                "local": f"Sala {evento.get('id_sala')}"
            })

    # Consolidar informações e organizar resultados por data e horário
    itens_filtrados.sort(key=lambda x: (x.get("data", ""), x.get("horario_inicio", "")))

    return {
        "sucesso": True,
        "filtro_mes_ano": mes_ano or "Todos",
        "total_eventos": len([i for i in itens_filtrados if i["tipo"] == "evento"]),
        "total_reservas": len([i for i in itens_filtrados if i["tipo"] == "reserva"]),
        "agenda": itens_filtrados
    }
