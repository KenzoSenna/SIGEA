from fastapi import HTTPException, status

from models import Usuario


def exigir_tipo(usuario: Usuario, *tipos_permitidos: str) -> None:
    if usuario.tipo not in tipos_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "sucesso": False,
                "mensagem": f"Permissão insuficiente — ação restrita a: {', '.join(tipos_permitidos)}",
            },
        )


def exigir_dono_ou_coordenador(
    usuario: Usuario, id_dono: int | None, acao: str
) -> None:
    if usuario.tipo == "coordenador":
        return

    if id_dono is None or usuario.id_usuario != id_dono:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "sucesso": False,
                "mensagem": f"Permissão insuficiente — apenas o responsável ou um coordenador pode {acao}",
            },
        )
