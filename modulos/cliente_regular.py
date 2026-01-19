"""
Módulo de la subclase ClienteRegular.
Representa clientes regulares con sistema de puntos de acumulación.
"""

from .cliente import Cliente
from .validaciones import validar_numero_positivo


class ClienteRegular(Cliente):
    """
    Subclase que representa un cliente regular con puntos acumulados.

    Atributos heredados:
        nombre, email, teléfono, dirección (de Cliente)

    Atributos propios:
        __puntos_acumulados (int): Puntos acumulados por compras
    """

    def __init__(self, nombre, email, telefono, direccion, puntos_acumulados=0):
        """
        Inicializa un cliente regular.

        Args:
            nombre (str): Nombre del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente
            direccion (str): Dirección del cliente
            puntos_acumulados (int): Puntos iniciales (default: 0)
        """
        super().__init__(nombre, email, telefono, direccion)
        validar_numero_positivo(
            puntos_acumulados, "puntos_acumulados", permitir_cero=True
        )
        self.__puntos_acumulados = int(puntos_acumulados)

    @property
    def puntos_acumulados(self):
        """Obtiene los puntos acumulados."""
        return self.__puntos_acumulados

    @puntos_acumulados.setter
    def puntos_acumulados(self, valor):
        """Establece los puntos acumulados con validación."""
        validar_numero_positivo(valor, "puntos_acumulados", permitir_cero=True)
        self.__puntos_acumulados = int(valor)

    def acumular_puntos(self, cantidad):
        """
        Suma puntos a los acumulados.

        Args:
            cantidad (int): Cantidad de puntos a agregar

        Raises:
            DatosInvalidosError: Si la cantidad es inválida
        """
        validar_numero_positivo(cantidad, "cantidad de puntos", permitir_cero=False)
        self.__puntos_acumulados += int(cantidad)

    def canjear_puntos(self, cantidad):
        """
        Canjea puntos (descuenta del total).

        Args:
            cantidad (int): Cantidad de puntos a canjear

        Returns:
            bool: True si fue exitoso

        Raises:
            DatosInvalidosError: Si no hay suficientes puntos
        """
        validar_numero_positivo(cantidad, "cantidad de puntos", permitir_cero=False)
        cantidad = int(cantidad)

        if cantidad > self.__puntos_acumulados:
            raise ValueError(
                f"No hay suficientes puntos. "
                f"Disponibles: {self.__puntos_acumulados}, "
                f"Solicitados: {cantidad}"
            )

        self.__puntos_acumulados -= cantidad
        return True

    def mostrar_info(self):
        """
        Sobrescribe el método de la clase base para incluir puntos.
        Demuestra polimorfismo.

        Returns:
            str: Información completa del cliente regular
        """
        info_base = super().mostrar_info()
        return (
            f"=== CLIENTE REGULAR ===\n"
            f"{info_base}\n"
            f"Puntos Acumulados: {self.__puntos_acumulados}"
        )

    def to_dict(self):
        """Convierte el cliente regular a diccionario."""
        datos = super().to_dict()
        datos["tipo"] = "Regular"
        datos["puntos_acumulados"] = self.__puntos_acumulados
        return datos

    def __repr__(self):
        """Representación técnica para debugging."""
        return (
            f"ClienteRegular(nombre='{self.nombre}', "
            f"email='{self.email}', "
            f"puntos={self.__puntos_acumulados})"
        )
