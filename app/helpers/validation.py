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
