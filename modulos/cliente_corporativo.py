"""
Módulo de la subclase ClienteCorporativo.
Representa clientes corporativos/empresariales del sistema.
"""

from .cliente import Cliente
from .validaciones import validar_texto_no_vacio, validar_rut


class ClienteCorporativo(Cliente):
    """
    Subclase que representa un cliente corporativo/empresarial.

    Atributos heredados:
        nombre, email, teléfono, dirección (de Cliente)

    Atributos propios:
        __empresa (str): Nombre de la empresa
        __rut_empresa (str): RUT de la empresa con validación
        __contacto_principal (str): Nombre del contacto principal
    """

    def __init__(
        self,
        nombre,
        email,
        telefono,
        direccion,
        empresa,
        rut_empresa,
        contacto_principal,
    ):
        """
        Inicializa un cliente corporativo.

        Args:
            nombre (str): Nombre del cliente (generalmente la empresa)
            email (str): Email corporativo
            telefono (str): Teléfono corporativo
            direccion (str): Dirección de la oficina
            empresa (str): Nombre de la empresa
            rut_empresa (str): RUT de la empresa (con validación)
            contacto_principal (str): Nombre del contacto principal

        Raises:
            RutInvalidoError: Si el RUT es inválido
            DatosInvalidosError: Si hay campos vacíos
        """
        super().__init__(nombre, email, telefono, direccion)
        validar_texto_no_vacio(empresa, "empresa")
        validar_rut(rut_empresa)
        validar_texto_no_vacio(contacto_principal, "contacto_principal")

        self.__empresa = empresa
        self.__rut_empresa = rut_empresa.replace(".", "").upper()
        self.__contacto_principal = contacto_principal

    @property
    def empresa(self):
        """Obtiene el nombre de la empresa."""
        return self.__empresa

    @empresa.setter
    def empresa(self, valor):
        """Establece el nombre de la empresa."""
        validar_texto_no_vacio(valor, "empresa")
        self.__empresa = valor

    @property
    def rut_empresa(self):
        """Obtiene el RUT de la empresa."""
        return self.__rut_empresa

    @rut_empresa.setter
    def rut_empresa(self, valor):
        """Establece el RUT con validación."""
        validar_rut(valor)
        self.__rut_empresa = valor.replace(".", "").upper()

    @property
    def contacto_principal(self):
        """Obtiene el contacto principal."""
        return self.__contacto_principal

    @contacto_principal.setter
    def contacto_principal(self, valor):
        """Establece el contacto principal."""
        validar_texto_no_vacio(valor, "contacto_principal")
        self.__contacto_principal = valor

    def generar_factura_corporativa(self, numero_factura, monto, descripcion=""):
        """
        Genera un resumen de factura corporativa.

        Args:
            numero_factura (int): Número de factura
            monto (float): Monto de la factura
            descripcion (str): Descripción del servicio/producto

        Returns:
            str: Resumen de factura formateado
        """
        from datetime import datetime

        factura = (
            f"\n{'='*50}\n"
            f"FACTURA CORPORATIVA\n"
            f"{'='*50}\n"
            f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Número de Factura: {numero_factura}\n"
            f"\nEMPRESA:\n"
            f"  Nombre: {self.__empresa}\n"
            f"  RUT: {self._formatear_rut()}\n"
            f"  Contacto: {self.__contacto_principal}\n"
            f"  Email: {self.email}\n"
            f"  Teléfono: {self.telefono}\n"
            f"  Dirección: {self.direccion}\n"
            f"\nDETALLES:\n"
            f"  Descripción: {descripcion if descripcion else 'Sin descripción'}\n"
            f"  Monto Total: ${monto:,.2f}\n"
            f"{'='*50}\n"
        )
        return factura

    def _formatear_rut(self):
        """Formatea el RUT con puntos y guión."""
        rut_limpio = self.__rut_empresa.replace("-", "").replace(".", "")
        if len(rut_limpio) < 2:
            return self.__rut_empresa

        numero = rut_limpio[:-1]
        digito = rut_limpio[-1]

        # Formatear con puntos
        partes = []
        for i, digito_num in enumerate(reversed(numero)):
            if i > 0 and i % 3 == 0:
                partes.append(".")
            partes.append(digito_num)

        numero_formateado = "".join(reversed(partes))
        return f"{numero_formateado}-{digito}"

    def obtener_datos_tributarios(self):
        """
        Retorna información tributaria de la empresa.

        Returns:
            dict: Datos tributarios
        """
        return {
            "empresa": self.__empresa,
            "rut": self._formatear_rut(),
            "contacto": self.__contacto_principal,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion,
        }

    def mostrar_info(self):
        """
        Sobrescribe el método de la clase base con información corporativa.

        Returns:
            str: Información completa del cliente corporativo
        """
        info_base = super().mostrar_info()
        return (
            f"=== CLIENTE CORPORATIVO ===\n"
            f"{info_base}\n"
            f"Empresa: {self.__empresa}\n"
            f"RUT Empresa: {self._formatear_rut()}\n"
            f"Contacto Principal: {self.__contacto_principal}"
        )

    def to_dict(self):
        """Convierte el cliente corporativo a diccionario."""
        datos = super().to_dict()
        datos["tipo"] = "Corporativo"
        datos["empresa"] = self.__empresa
        datos["rut_empresa"] = self.__rut_empresa
        datos["contacto_principal"] = self.__contacto_principal
        return datos

    def __repr__(self):
        """Representación técnica para debugging."""
        return (
            f"ClienteCorporativo(nombre='{self.nombre}', "
            f"empresa='{self.__empresa}', "
            f"rut='{self.__rut_empresa}')"
        )
