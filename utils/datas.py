from datetime import date, datetime, time


def converter_para_datetime(data: date, hora: time | str) -> datetime:
    if isinstance(hora, str):
        hora = datetime.strptime(hora, "%H:%M:%S").time()
    return datetime.combine(data, hora)
