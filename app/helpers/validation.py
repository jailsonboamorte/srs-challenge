from log import logger


def validate_cpf(cpf: dict) -> bool:
    # Remove any non-digit characters
    cpf = "".join(filter(str.isdigit, str(cpf)))

    # Check if CPF has 11 digits
    if len(cpf) != 11:
        return False

    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        return False

    # Calculate first verification digit
    sum1 = 0
    for i in range(9):
        sum1 += int(cpf[i]) * (10 - i)

    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1

    # Check first verification digit
    if int(cpf[9]) != digit1:
        return False

    # Calculate second verification digit
    sum2 = 0
    for i in range(10):
        sum2 += int(cpf[i]) * (11 - i)

    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2

    # Check second verification digit
    if int(cpf[10]) != digit2:
        return False

    return True


def validate_cnpj(cnpj):
    # Remove any non-digit characters
    cnpj = "".join(filter(str.isdigit, str(cnpj)))

    # Check if CNPJ has 14 digits
    if len(cnpj) != 14:
        return False

    # Check if all digits are the same (invalid CNPJ)
    if cnpj == cnpj[0] * 14:
        return False

    # Calculate first verification digit
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum1 = 0
    for i in range(12):
        sum1 += int(cnpj[i]) * weights1[i]

    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1

    # Check first verification digit
    if int(cnpj[12]) != digit1:
        return False

    # Calculate second verification digit
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum2 = 0
    for i in range(13):
        sum2 += int(cnpj[i]) * weights2[i]

    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2

    # Check second verification digit
    if int(cnpj[13]) != digit2:
        return False
    return True
