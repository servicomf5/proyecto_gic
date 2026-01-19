"""
Paquete modulos del Gestor Inteligente de Clientes.
Contiene todas las clases y funciones del sistema.
"""

from .cliente import Cliente
from .cliente_regular import ClienteRegular
from .cliente_premium import ClientePremium
from .cliente_corporativo import ClienteCorporativo
from .gestor_clientes import GestorClientes
from .excepciones import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    ClienteExistenteError,
    ClienteNoEncontradoError,
    DatosInvalidosError,
    RutInvalidoError,
)
from .validaciones import (
    validar_email,
    validar_telefono,
    validar_rut,
    validar_texto_no_vacio,
    validar_numero_positivo,
    validar_rango_numero,
)

__all__ = [
    "Cliente",
    "ClienteRegular",
    "ClientePremium",
    "ClienteCorporativo",
    "GestorClientes",
    "EmailInvalidoError",
    "TelefonoInvalidoError",
    "ClienteExistenteError",
    "ClienteNoEncontradoError",
    "DatosInvalidosError",
    "RutInvalidoError",
    "validar_email",
    "validar_telefono",
    "validar_rut",
    "validar_texto_no_vacio",
    "validar_numero_positivo",
    "validar_rango_numero",
]
