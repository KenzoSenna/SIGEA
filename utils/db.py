def tratar_integrity_error(e) -> str:
    
    msg = str(e.orig) if hasattr(e, "orig") and e.orig else str(e)
    if "1062" in msg or "Duplicate entry" in msg:
        return "Registro duplicado — este valor já existe no sistema"
    if "1452" in msg or "foreign key constraint" in msg.lower():
        return "Referência inválida — registro relacionado não encontrado"
    return "Violação de integridade de dados"
