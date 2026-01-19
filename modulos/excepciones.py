"""
Módulo de excepciones personalizadas para el Gestor Inteligente de Clientes.
Contiene todas las excepciones específicas del sistema.
"""


class EmailInvalidoError(Exception):
    """Excepción lanzada cuando el formato del email es inválido."""

    pass


class TelefonoInvalidoError(Exception):
    """Excepción lanzada cuando el formato del teléfono es inválido."""

    pass


class ClienteExistenteError(Exception):
    """Excepción lanzada cuando se intenta registrar un cliente que ya existe."""

    pass


class ClienteNoEncontradoError(Exception):
    """Excepción lanzada cuando no se encuentra el cliente buscado."""

    pass


class DatosInvalidosError(Exception):
    """Excepción lanzada para validaciones generales de datos."""

    pass


class RutInvalidoError(Exception):
    """Excepción lanzada cuando el formato del RUT es inválido."""

    pass
