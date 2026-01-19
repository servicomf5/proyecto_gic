"""
Módulo del Gestor de Clientes.
Implementa todas las operaciones CRUD y manejo de archivos del sistema.
"""

import csv
import logging
import os
import shutil
from datetime import datetime
from .cliente import Cliente
from .cliente_regular import ClienteRegular
from .cliente_premium import ClientePremium
from .cliente_corporativo import ClienteCorporativo
from .excepciones import (
    ClienteExistenteError,
    ClienteNoEncontradoError,
    DatosInvalidosError,
)


class GestorClientes:
    """
    Gestor central de clientes que implementa operaciones CRUD,
    manejo de archivos y logging.

    Atributos privados:
        __clientes (list): Lista de objetos Cliente
        __ruta_csv (str): Ruta del archivo CSV
        __ruta_log (str): Ruta del archivo de log
        __logger (logging.Logger): Logger del sistema
    """

    def __init__(self, ruta_csv="datos/clientes.csv", ruta_log="logs/app.log"):
        """
        Inicializa el gestor de clientes.

        Args:
            ruta_csv (str): Ruta del archivo CSV
            ruta_log (str): Ruta del archivo de log
        """
        self.__clientes = []
        self.__ruta_csv = ruta_csv
        self.__ruta_log = ruta_log

        # Configurar logging
        self.__logger = self._configurar_logging()

        # Crear directorios si no existen
        self._crear_directorios()

        self.__logger.info("Gestor de Clientes inicializado")

    # ======================== LOGGING ========================

    def _configurar_logging(self):
        """
        Configura el sistema de logging.

        Returns:
            logging.Logger: Logger configurado
        """
        # Crear directorio de logs si no existe
        if not os.path.exists("logs"):
            os.makedirs("logs")

        logger = logging.getLogger("GestorClientes")
        logger.setLevel(logging.DEBUG)

        # Handler para archivo
        handler_archivo = logging.FileHandler(self.__ruta_log, encoding="utf-8")
        handler_archivo.setLevel(logging.DEBUG)

        # Formato
        formato = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler_archivo.setFormatter(formato)

        # Evitar duplicados
        if not logger.handlers:
            logger.addHandler(handler_archivo)

        return logger

    def _crear_directorios(self):
        """Crea los directorios necesarios si no existen."""
        directorios = ["datos", "reportes", "logs"]
        for directorio in directorios:
            if not os.path.exists(directorio):
                os.makedirs(directorio)

    def registrar_actividad(self, accion, mensaje):
        """
        Registra una actividad en el archivo de log.

        Args:
            accion (str): Tipo de acción (ALTA, BAJA, CONSULTA, ERROR, etc.)
            mensaje (str): Mensaje descriptivo
        """
        nivel_log = {
            "ALTA": logging.INFO,
            "BAJA": logging.INFO,
            "CONSULTA": logging.DEBUG,
            "ACTUALIZACIÓN": logging.INFO,
            "ERROR": logging.ERROR,
            "EXPORTACIÓN": logging.INFO,
            "IMPORTACIÓN": logging.INFO,
        }

        nivel = nivel_log.get(accion, logging.INFO)
        log_mensaje = f"{accion} - {mensaje}"
        self.__logger.log(nivel, log_mensaje)

    # ======================== OPERACIONES CRUD ========================

    def agregar_cliente(self, cliente):
        """
        Agrega un nuevo cliente a la lista.

        Args:
            cliente (Cliente): Objeto cliente a agregar

        Raises:
            ClienteExistenteError: Si el cliente ya existe
            DatosInvalidosError: Si el cliente es inválido
        """
        if not isinstance(cliente, Cliente):
            self.registrar_actividad("ERROR", "Intento de agregar objeto no cliente")
            raise DatosInvalidosError("El objeto debe ser una instancia de Cliente")

        # Verificar si ya existe
        if self.buscar_cliente(cliente.email):
            mensaje = f"Cliente con email {cliente.email} ya existe"
            self.registrar_actividad("ERROR", mensaje)
            raise ClienteExistenteError(mensaje)

        self.__clientes.append(cliente)
        self.registrar_actividad("ALTA", f"Cliente registrado: {cliente.email}")

    def buscar_cliente(self, email_o_nombre):
        """
        Busca un cliente por email o nombre (case-insensitive).

        Args:
            email_o_nombre (str): Email o nombre a buscar

        Returns:
            Cliente: Objeto cliente encontrado o None
        """
        busqueda = email_o_nombre.lower()

        for cliente in self.__clientes:
            # Búsqueda por email
            if cliente.email == busqueda.lower():
                self.registrar_actividad(
                    "CONSULTA", f"Cliente encontrado: {cliente.email}"
                )
                return cliente
            # Búsqueda por nombre
            if cliente.nombre.lower().find(busqueda) != -1:
                self.registrar_actividad(
                    "CONSULTA", f"Cliente encontrado por nombre: {cliente.nombre}"
                )
                return cliente

        self.registrar_actividad("CONSULTA", f"Cliente no encontrado: {email_o_nombre}")
        return None

    def listar_clientes(self):
        """
        Retorna la lista completa de clientes.

        Returns:
            list: Lista de objetos Cliente
        """
        self.registrar_actividad(
            "CONSULTA", f"Listado solicitado: {len(self.__clientes)} clientes"
        )
        return self.__clientes.copy()

    def actualizar_cliente(self, email, nuevos_datos):
        """
        Actualiza los datos de un cliente existente.

        Args:
            email (str): Email del cliente a actualizar
            nuevos_datos (dict): Diccionario con campos a actualizar

        Returns:
            bool: True si se actualizó correctamente

        Raises:
            ClienteNoEncontradoError: Si el cliente no existe
        """
        cliente = self.buscar_cliente(email)

        if not cliente:
            self.registrar_actividad(
                "ERROR", f"Intento de actualizar cliente inexistente: {email}"
            )
            raise ClienteNoEncontradoError(f"Cliente con email {email} no encontrado")

        campos_actualizados = []

        try:
            for campo, valor in nuevos_datos.items():
                if hasattr(cliente, campo):
                    setattr(cliente, campo, valor)
                    campos_actualizados.append(f"{campo}={valor}")

            mensaje = f"Cliente {email} actualizado: {', '.join(campos_actualizados)}"
            self.registrar_actividad("ACTUALIZACIÓN", mensaje)
            return True

        except Exception as e:
            self.registrar_actividad(
                "ERROR", f"Error actualizando cliente {email}: {str(e)}"
            )
            raise

    def eliminar_cliente(self, email):
        """
        Elimina un cliente de la lista.

        Args:
            email (str): Email del cliente a eliminar

        Returns:
            bool: True si se eliminó correctamente

        Raises:
            ClienteNoEncontradoError: Si el cliente no existe
        """
        cliente = self.buscar_cliente(email)

        if not cliente:
            self.registrar_actividad(
                "ERROR", f"Intento de eliminar cliente inexistente: {email}"
            )
            raise ClienteNoEncontradoError(f"Cliente con email {email} no encontrado")

        self.__clientes.remove(cliente)
        self.registrar_actividad("BAJA", f"Cliente eliminado: {email}")
        return True

    # ======================== OPERACIONES CON ARCHIVOS ========================

    def exportar_a_csv(self):
        """
        Exporta todos los clientes a un archivo CSV.

        Returns:
            bool: True si se exportó correctamente
        """
        try:
            self._crear_directorios()

            with open(self.__ruta_csv, "w", newline="", encoding="utf-8") as archivo:
                # Escribir encabezado
                encabezados = [
                    "tipo",
                    "nombre",
                    "email",
                    "telefono",
                    "direccion",
                    "campo_extra1",
                    "campo_extra2",
                    "campo_extra3",
                ]
                writer = csv.DictWriter(archivo, fieldnames=encabezados)
                writer.writeheader()

                # Escribir clientes
                for cliente in self.__clientes:
                    fila = self._cliente_a_fila_csv(cliente)
                    writer.writerow(fila)

            self.registrar_actividad(
                "EXPORTACIÓN", f"Exportados {len(self.__clientes)} clientes a CSV"
            )
            return True

        except Exception as e:
            self.registrar_actividad("ERROR", f"Error exportando CSV: {str(e)}")
            raise

    def _cliente_a_fila_csv(self, cliente):
        """
        Convierte un cliente a una fila de CSV.

        Args:
            cliente (Cliente): Cliente a convertir

        Returns:
            dict: Fila para CSV
        """
        fila = {
            "tipo": "",
            "nombre": cliente.nombre,
            "email": cliente.email,
            "telefono": cliente.telefono,
            "direccion": cliente.direccion,
            "campo_extra1": "",
            "campo_extra2": "",
            "campo_extra3": "",
        }

        if isinstance(cliente, ClienteRegular):
            fila["tipo"] = "Regular"
            fila["campo_extra1"] = cliente.puntos_acumulados

        elif isinstance(cliente, ClientePremium):
            fila["tipo"] = "Premium"
            fila["campo_extra1"] = cliente.descuento_exclusivo
            fila["campo_extra2"] = cliente.fecha_membresia

        elif isinstance(cliente, ClienteCorporativo):
            fila["tipo"] = "Corporativo"
            fila["campo_extra1"] = cliente.empresa
            fila["campo_extra2"] = cliente.rut_empresa
            fila["campo_extra3"] = cliente.contacto_principal

        return fila

    def importar_desde_csv(self, ruta):
        """
        Importa clientes desde un archivo CSV.

        Args:
            ruta (str): Ruta del archivo CSV a importar

        Returns:
            dict: Estadísticas de importación {total, exitosos, errores}

        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        try:
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"Archivo {ruta} no encontrado")

            # Hacer backup antes de importar
            self._hacer_backup()

            estadisticas = {"total": 0, "exitosos": 0, "errores": 0, "duplicados": 0}

            with open(ruta, "r", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)

                for fila in reader:
                    estadisticas["total"] += 1

                    try:
                        cliente = self._fila_csv_a_cliente(fila)

                        # Verificar si ya existe
                        if self.buscar_cliente(cliente.email):
                            estadisticas["duplicados"] += 1
                            continue

                        self.__clientes.append(cliente)
                        estadisticas["exitosos"] += 1

                    except Exception as e:
                        estadisticas["errores"] += 1
                        self.registrar_actividad(
                            "ERROR", f"Error importando fila: {str(e)}"
                        )

            self.registrar_actividad(
                "IMPORTACIÓN", f"Importación completada: {estadisticas}"
            )
            return estadisticas

        except Exception as e:
            self.registrar_actividad("ERROR", f"Error importando CSV: {str(e)}")
            raise

    def _fila_csv_a_cliente(self, fila):
        """
        Convierte una fila de CSV a un objeto Cliente.

        Args:
            fila (dict): Fila del CSV

        Returns:
            Cliente: Objeto cliente creado
        """
        tipo = fila.get("tipo", "").strip()
        nombre = fila.get("nombre", "").strip()
        email = fila.get("email", "").strip()
        telefono = fila.get("telefono", "").strip()
        direccion = fila.get("direccion", "").strip()

        if tipo == "Regular":
            puntos = int(fila.get("campo_extra1", 0) or 0)
            return ClienteRegular(nombre, email, telefono, direccion, puntos)

        elif tipo == "Premium":
            descuento = float(fila.get("campo_extra1", 10) or 10)
            fecha = fila.get("campo_extra2", None)
            return ClientePremium(nombre, email, telefono, direccion, descuento, fecha)

        elif tipo == "Corporativo":
            empresa = fila.get("campo_extra1", "").strip()
            rut = fila.get("campo_extra2", "").strip()
            contacto = fila.get("campo_extra3", "").strip()
            return ClienteCorporativo(
                nombre, email, telefono, direccion, empresa, rut, contacto
            )
        else:
            return Cliente(nombre, email, telefono, direccion)

    def _hacer_backup(self):
        """Crea un backup del CSV actual antes de importar."""
        try:
            if os.path.exists(self.__ruta_csv):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"datos/clientes_backup_{timestamp}.csv"
                shutil.copy2(self.__ruta_csv, backup_path)
                self.registrar_actividad("INFORMACIÓN", f"Backup creado: {backup_path}")
        except Exception as e:
            self.registrar_actividad("ADVERTENCIA", f"Error creando backup: {str(e)}")

    # ======================== REPORTES ========================

    def generar_reporte(self):
        """
        Genera un reporte estadístico del sistema.

        Returns:
            str: Contenido del reporte
        """
        estadisticas = self._calcular_estadisticas()

        contenido = self._generar_contenido_reporte(estadisticas)

        try:
            self._crear_directorios()

            ruta_reporte = "reportes/resumen.txt"
            with open(ruta_reporte, "w", encoding="utf-8") as archivo:
                archivo.write(contenido)

            self.registrar_actividad("EXPORTACIÓN", f"Reporte generado: {ruta_reporte}")

            return contenido

        except Exception as e:
            self.registrar_actividad("ERROR", f"Error generando reporte: {str(e)}")
            raise

    def _calcular_estadisticas(self):
        """
        Calcula estadísticas del sistema.

        Returns:
            dict: Estadísticas calculadas
        """
        regulares = [c for c in self.__clientes if isinstance(c, ClienteRegular)]
        premium = [c for c in self.__clientes if isinstance(c, ClientePremium)]
        corporativos = [c for c in self.__clientes if isinstance(c, ClienteCorporativo)]

        return {
            "total": len(self.__clientes),
            "regulares": len(regulares),
            "premium": len(premium),
            "corporativos": len(corporativos),
            "max_puntos": max([c.puntos_acumulados for c in regulares], default=0),
            "max_descuento": max([c.descuento_exclusivo for c in premium], default=0),
            "cliente_max_puntos": next(
                (
                    c.nombre
                    for c in regulares
                    if c.puntos_acumulados
                    == max([x.puntos_acumulados for x in regulares], default=0)
                ),
                "N/A",
            ),
            "cliente_max_descuento": next(
                (
                    c.nombre
                    for c in premium
                    if c.descuento_exclusivo
                    == max([x.descuento_exclusivo for x in premium], default=0)
                ),
                "N/A",
            ),
        }

    def _generar_contenido_reporte(self, estadisticas):
        """
        Genera el contenido del reporte.

        Args:
            estadisticas (dict): Estadísticas calculadas

        Returns:
            str: Contenido formateado
        """
        linea = "=" * 50
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        contenido = f"""{linea}
REPORTE DEL GESTOR INTELIGENTE DE CLIENTES (GIC)
{linea}
Fecha y Hora: {fecha_hora}

ESTADÍSTICAS GENERALES:
{linea}
Total de Clientes: {estadisticas['total']}

Clientes Regulares: {estadisticas['regulares']}
Clientes Premium: {estadisticas['premium']}
Clientes Corporativos: {estadisticas['corporativos']}

ESTADÍSTICAS AVANZADAS:
{linea}
Cliente Regular con más puntos: {estadisticas['cliente_max_puntos']}
  (Puntos: {estadisticas['max_puntos']})

Cliente Premium con mayor descuento: {estadisticas['cliente_max_descuento']}
  (Descuento: {estadisticas['max_descuento']}%)

{linea}
"""
        return contenido
