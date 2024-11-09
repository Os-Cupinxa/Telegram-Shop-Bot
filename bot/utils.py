from datetime import datetime


def format_date(date_string: str) -> str:
    try:
        created_datetime = datetime.fromisoformat(date_string)
        return created_datetime.strftime("%d/%m/%Y")

    except ValueError:
        return "Data inválida"
