import re
from datetime import datetime


def format_date(date_string: str) -> str:
    try:
        created_datetime = datetime.fromisoformat(date_string)
        return created_datetime.strftime("%d/%m/%Y")

    except ValueError:
        return "Data inválida"


def is_cpf_valid(cpf):
    if not isinstance(cpf, str):
        return False

    cpf = re.sub("[^0-9]", '', cpf)

    if (cpf == '00000000000'
            or cpf == '11111111111'
            or cpf == '22222222222'
            or cpf == '33333333333'
            or cpf == '44444444444'
            or cpf == '55555555555'
            or cpf == '66666666666'
            or cpf == '77777777777'
            or cpf == '88888888888'
            or cpf == '99999999999'):
        return False

    if len(cpf) != 11:
        return False

    total_sum = 0
    weight = 10

    for n in range(9):
        total_sum = total_sum + int(cpf[n]) * weight

        weight = weight - 1

    verifying_digit = 11 - total_sum % 11

    if verifying_digit > 9:
        first_verifying_digit = 0
    else:
        first_verifying_digit = verifying_digit

    total_sum = 0
    weight = 11
    for n in range(10):
        total_sum = total_sum + int(cpf[n]) * weight

        weight = weight - 1

    verifying_digit = 11 - total_sum % 11

    if verifying_digit > 9:
        second_verifying_digit = 0
    else:
        second_verifying_digit = verifying_digit

    if cpf[-2:] == "%s%s" % (first_verifying_digit, second_verifying_digit):
        return True
    return False
