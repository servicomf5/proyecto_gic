"""
Módulo de validaciones para el Gestor Inteligente de Clientes.
Contiene funciones de validación con expresiones regulares (regex).
"""

import re
from .excepciones import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    RutInvalidoError,
    DatosInvalidosError,
)


def validar_email(email):
    """
    Valida el formato de un email.

    Args:
        email (str): Email a validar

    Returns:
        bool: True si es válido

    Raises:
        EmailInvalidoError: Si el email no cumple el formato esperado
    """
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(patron, email):
        raise EmailInvalidoError(f"El email '{email}' no tiene un formato válido.")
    return True


def validar_telefono(telefono):
    """
    Valida el formato de un teléfono chileno.
    Acepta formatos: +56912345678, +56 9 1234 5678, 0912345678, etc.

    Args:
        telefono (str): Teléfono a validar

    Returns:
        bool: True si es válido

    Raises:
        TelefonoInvalidoError: Si el teléfono no cumple el formato esperado
    """
    # Remover espacios
    telefono_limpio = telefono.replace(" ", "").replace("-", "")

    # Patrón para teléfono chileno
    patron = r"^\+?56[9]?\d{8}$|^0?9\d{8}$"
    if not re.match(patron, telefono_limpio):
        raise TelefonoInvalidoError(
            f"El teléfono '{telefono}' no tiene un formato válido. "
            "Use: +56912345678 o 0912345678"
        )
    return True


def validar_rut(rut):
    """
    Valida el formato del RUT chileno con dígito verificador (algoritmo módulo 11).
    Formato: XX.XXX.XXX-K donde X es número y K es dígito o letra

    Args:
        rut (str): RUT a validar (ej: "12.345.678-9" o "12345678-9")

    Returns:
        bool: True si es válido

    Raises:
        RutInvalidoError: Si el RUT es inválido
    """
    # Remover puntos y espacios
    rut_limpio = rut.replace(".", "").replace(" ", "").upper()

    # Validar formato básico
    if not re.match(r"^\d{7,8}-[\dK]$", rut_limpio):
        raise RutInvalidoError(
            f"El RUT '{rut}' no tiene un formato válido. " "Use: 12.345.678-9"
        )

    # Separar número y dígito verificador
    partes = rut_limpio.split("-")
    numero_str = partes[0]
    digito_esperado = partes[1]

    # Calcular dígito verificador (módulo 11)
    numero = int(numero_str)
    suma = 0
    multiplicador = 2

    while numero > 0:
        suma += (numero % 10) * multiplicador
        numero //= 10
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    digito_verificador = 11 - (suma % 11)

    if digito_verificador == 11:
        digito_calculado = "0"
    elif digito_verificador == 10:
        digito_calculado = "K"
    else:
        digito_calculado = str(digito_verificador)

    if digito_esperado != digito_calculado:
        raise RutInvalidoError(
            f"El RUT '{rut}' tiene un dígito verificador inválido. "
            f"Esperado: {digito_calculado}, Recibido: {digito_esperado}"
        )

    return True


def validar_texto_no_vacio(texto, campo):
    """
    Valida que un texto no esté vacío.

    Args:
        texto (str): Texto a validar
        campo (str): Nombre del campo (para el mensaje de error)

    Returns:
        bool: True si es válido

    Raises:
        DatosInvalidosError: Si el texto está vacío
    """
    if not texto or not isinstance(texto, str) or texto.strip() == "":
        raise DatosInvalidosError(f"El campo '{campo}' no puede estar vacío.")
    return True


def validar_numero_positivo(numero, campo, permitir_cero=False):
    """
    Valida que un número sea positivo.

    Args:
        numero (int/float): Número a validar
        campo (str): Nombre del campo (para el mensaje de error)
        permitir_cero (bool): Si se permite 0 como válido

    Returns:
        bool: True si es válido

    Raises:
        DatosInvalidosError: Si el número no es válido
    """
    try:
        num = float(numero)
        if permitir_cero and num >= 0:
            return True
        elif num > 0:
            return True
        else:
            raise ValueError
    except (ValueError, TypeError):
        min_valor = "0" if permitir_cero else "mayor a 0"
        raise DatosInvalidosError(f"El campo '{campo}' debe ser un número {min_valor}.")


def validar_rango_numero(numero, campo, minimo, maximo):
    """
    Valida que un número esté dentro de un rango específico.

    Args:
        numero (int/float): Número a validar
        campo (str): Nombre del campo
        minimo (int/float): Valor mínimo permitido
        maximo (int/float): Valor máximo permitido

    Returns:
        bool: True si es válido

    Raises:
        DatosInvalidosError: Si está fuera de rango
    """
    try:
        num = float(numero)
        if minimo <= num <= maximo:
            return True
        else:
            raise ValueError
    except (ValueError, TypeError):
        raise DatosInvalidosError(
            f"El campo '{campo}' debe estar entre {minimo} y {maximo}."
        )
