"""
Módulo de la subclase ClientePremium.
Representa clientes premium con descuentos exclusivos y beneficios especiales.
"""

from datetime import datetime
from .cliente import Cliente
from .validaciones import validar_rango_numero


class ClientePremium(Cliente):
    """
    Subclase que representa un cliente premium con beneficios exclusivos.

    Atributos heredados:
        nombre, email, teléfono, dirección (de Cliente)

    Atributos propios:
        __descuento_exclusivo (float): Descuento en porcentaje (0-100)
        __fecha_membresia (str): Fecha de inicio de membresía
    """

    def __init__(
        self,
        nombre,
        email,
        telefono,
        direccion,
        descuento_exclusivo=10.0,
        fecha_membresia=None,
    ):
        """
        Inicializa un cliente premium.

        Args:
            nombre (str): Nombre del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente
            direccion (str): Dirección del cliente
            descuento_exclusivo (float): Descuento en % (0-100, default: 10)
            fecha_membresia (str): Fecha en formato YYYY-MM-DD (default: hoy)
        """
        super().__init__(nombre, email, telefono, direccion)
        validar_rango_numero(descuento_exclusivo, "descuento_exclusivo", 0, 100)

        self.__descuento_exclusivo = float(descuento_exclusivo)

        if fecha_membresia is None:
            self.__fecha_membresia = datetime.now().strftime("%Y-%m-%d")
        else:
            # Validar formato de fecha
            try:
                datetime.strptime(fecha_membresia, "%Y-%m-%d")
                self.__fecha_membresia = fecha_membresia
            except ValueError:
                raise ValueError("La fecha debe estar en formato YYYY-MM-DD")

    @property
    def descuento_exclusivo(self):
        """Obtiene el descuento exclusivo."""
        return self.__descuento_exclusivo

    @descuento_exclusivo.setter
    def descuento_exclusivo(self, valor):
        """Establece el descuento con validación."""
        validar_rango_numero(valor, "descuento_exclusivo", 0, 100)
        self.__descuento_exclusivo = float(valor)

    @property
    def fecha_membresia(self):
        """Obtiene la fecha de membresía."""
        return self.__fecha_membresia

    @fecha_membresia.setter
    def fecha_membresia(self, valor):
        """Establece la fecha de membresía con validación."""
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            self.__fecha_membresia = valor
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD")

    def beneficio_exclusivo(self):
        """
        Muestra los beneficios exclusivos del cliente premium.

        Returns:
            str: Descripción de beneficios
        """
        antiguedad_meses = self._calcular_antiguedad_meses()

        beneficios = [
            f"✓ Descuento exclusivo del {self.__descuento_exclusivo}%",
            "✓ Atención prioritaria 24/7",
            "✓ Envío gratis en todas las compras",
            "✓ Acceso a productos exclusivos",
            "✓ Asesoría personalizada",
            f"✓ Miembro desde {antiguedad_meses} meses",
        ]

        return "\n".join(beneficios)

    def _calcular_antiguedad_meses(self):
        """Calcula la antigüedad en meses."""
        fecha_inicio = datetime.strptime(self.__fecha_membresia, "%Y-%m-%d")
        fecha_actual = datetime.now()
        meses = (fecha_actual.year - fecha_inicio.year) * 12 + (
            fecha_actual.month - fecha_inicio.month
        )
        return max(0, meses)

    def aplicar_descuento(self, monto):
        """
        Calcula el monto con descuento aplicado.

        Args:
            monto (float): Monto original

        Returns:
            float: Monto con descuento
        """
        return monto * (1 - self.__descuento_exclusivo / 100)

    def mostrar_info(self):
        """
        Sobrescribe el método de la clase base para incluir beneficios premium.

        Returns:
            str: Información completa del cliente premium
        """
        info_base = super().mostrar_info()
        return (
            f"=== CLIENTE PREMIUM ===\n"
            f"{info_base}\n"
            f"Descuento Exclusivo: {self.__descuento_exclusivo}%\n"
            f"Fecha de Membresía: {self.__fecha_membresia}\n"
            f"Antigüedad: {self._calcular_antiguedad_meses()} meses"
        )

    def to_dict(self):
        """Convierte el cliente premium a diccionario."""
        datos = super().to_dict()
        datos["tipo"] = "Premium"
        datos["descuento_exclusivo"] = self.__descuento_exclusivo
        datos["fecha_membresia"] = self.__fecha_membresia
        return datos

    def __repr__(self):
        """Representación técnica para debugging."""
        return (
            f"ClientePremium(nombre='{self.nombre}', "
            f"email='{self.email}', "
            f"descuento={self.__descuento_exclusivo}%)"
        )
