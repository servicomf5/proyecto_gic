"""
Módulo de la clase base Cliente.
Define la estructura y comportamiento general de todos los clientes.
"""

from .validaciones import validar_email, validar_telefono, validar_texto_no_vacio


class Cliente:
    """
    Clase base que representa un cliente del sistema.

    Atributos privados:
        __nombre (str): Nombre del cliente
        __email (str): Email único del cliente
        __telefono (str): Número de teléfono
        __direccion (str): Dirección del cliente
    """

    def __init__(self, nombre, email, telefono, direccion):
        """
        Inicializa un cliente con validaciones.

        Args:
            nombre (str): Nombre del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente
            direccion (str): Dirección del cliente

        Raises:
            EmailInvalidoError: Si email es inválido
            TelefonoInvalidoError: Si teléfono es inválido
            DatosInvalidosError: Si campos están vacíos
        """
        validar_texto_no_vacio(nombre, "nombre")
        validar_email(email)
        validar_telefono(telefono)
        validar_texto_no_vacio(direccion, "dirección")

        self.__nombre = nombre
        self.__email = email.lower()
        self.__telefono = telefono
        self.__direccion = direccion

    # ======================== GETTERS ========================

    @property
    def nombre(self):
        """Obtiene el nombre del cliente."""
        return self.__nombre

    @property
    def email(self):
        """Obtiene el email del cliente."""
        return self.__email

    @property
    def telefono(self):
        """Obtiene el teléfono del cliente."""
        return self.__telefono

    @property
    def direccion(self):
        """Obtiene la dirección del cliente."""
        return self.__direccion

    # ======================== SETTERS ========================

    @nombre.setter
    def nombre(self, valor):
        """Establece el nombre con validación."""
        validar_texto_no_vacio(valor, "nombre")
        self.__nombre = valor

    @email.setter
    def email(self, valor):
        """Establece el email con validación."""
        validar_email(valor)
        self.__email = valor.lower()

    @telefono.setter
    def telefono(self, valor):
        """Establece el teléfono con validación."""
        validar_telefono(valor)
        self.__telefono = valor

    @direccion.setter
    def direccion(self, valor):
        """Establece la dirección con validación."""
        validar_texto_no_vacio(valor, "dirección")
        self.__direccion = valor

    # ======================== MÉTODOS ========================

    def mostrar_info(self):
        """
        Muestra la información del cliente de manera legible.
        Este método será sobrescrito en las subclases (polimorfismo).
        """
        return (
            f"Nombre: {self.__nombre}\n"
            f"Email: {self.__email}\n"
            f"Teléfono: {self.__telefono}\n"
            f"Dirección: {self.__direccion}"
        )

    def to_dict(self):
        """
        Convierte el cliente a un diccionario.
        Útil para exportar a CSV.

        Returns:
            dict: Diccionario con datos del cliente
        """
        return {
            "tipo": "Cliente",
            "nombre": self.__nombre,
            "email": self.__email,
            "telefono": self.__telefono,
            "direccion": self.__direccion,
        }

    def __str__(self):
        """Representación en string del cliente."""
        return f"Cliente(nombre='{self.__nombre}', " f"email='{self.__email}')"

    def __repr__(self):
        """Representación técnica para debugging."""
        return (
            f"Cliente(nombre='{self.__nombre}', "
            f"email='{self.__email}', "
            f"telefono='{self.__telefono}', "
            f"direccion='{self.__direccion}')"
        )
