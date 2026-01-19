"""
Módulo principal del Gestor Inteligente de Clientes (GIC).
Interfaz interactiva por consola para gestionar clientes.
"""

import sys
import os
from modulos import (
    GestorClientes,
    ClienteRegular,
    ClientePremium,
    ClienteCorporativo,
    EmailInvalidoError,
    TelefonoInvalidoError,
    ClienteExistenteError,
    ClienteNoEncontradoError,
    DatosInvalidosError,
    RutInvalidoError,
)


class InterfazGIC:
    """
    Interfaz de consola para el Gestor Inteligente de Clientes.
    """

    def __init__(self):
        """Inicializa la interfaz."""
        self.gestor = GestorClientes()
        self.ejecutando = True

        # Auto-cargar datos de prueba si existen
        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self):
        """Carga automáticamente el archivo CSV de entrada si existe."""
        ruta_entrada = "datos/clientes_entrada.csv"
        if os.path.exists(ruta_entrada):
            try:
                self.gestor.importar_desde_csv(ruta_entrada)
            except Exception:
                # Si hay error, simplemente continúa con lista vacía
                pass

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_encabezado(self):
        """Muestra el encabezado del programa."""
        print("\n" + "=" * 60)
        print("    GESTOR INTELIGENTE DE CLIENTES (GIC)")
        print("    Sistema de Gestión para SolutionTech")
        print("=" * 60 + "\n")

    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        self.limpiar_pantalla()
        self.mostrar_encabezado()
        print("OPCIONES DISPONIBLES:")
        print("-" * 60)
        print("1.  Registrar nuevo cliente")
        print("2.  Buscar cliente por email o nombre")
        print("3.  Listar todos los clientes")
        print("4.  Actualizar datos de cliente")
        print("5.  Eliminar cliente")
        print("6.  Exportar clientes a CSV")
        print("7.  Importar clientes desde CSV")
        print("8.  Generar reporte estadístico")
        print("9.  Ver ayuda")
        print("0.  Salir del programa")
        print("-" * 60)

    def seleccionar_opcion(self):
        """Solicita la opción al usuario."""
        try:
            opcion = input("\nSeleccione una opción (0-9): ").strip()
            return opcion
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario.")
            self.ejecutando = False
            return None

    def pausa(self):
        """Pausa la ejecución para que el usuario lea los mensajes."""
        input("\nPresione ENTER para continuar...")

    def ejecutar(self):
        """Ejecuta la interfaz principal."""
        while self.ejecutando:
            self.mostrar_menu_principal()
            opcion = self.seleccionar_opcion()

            if opcion is None:
                break

            operaciones = {
                "1": self.registrar_cliente,
                "2": self.buscar_cliente,
                "3": self.listar_clientes,
                "4": self.actualizar_cliente,
                "5": self.eliminar_cliente,
                "6": self.exportar_csv,
                "7": self.importar_csv,
                "8": self.generar_reporte,
                "9": self.mostrar_ayuda,
                "0": self.salir,
            }

            operacion = operaciones.get(opcion)
            if operacion:
                operacion()
            else:
                print("\n❌ Opción no válida. Intente nuevamente.")
                self.pausa()

    # ======================== OPERACIÓN 1: REGISTRAR ========================

    def registrar_cliente(self):
        """Permite registrar un nuevo cliente."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("REGISTRAR NUEVO CLIENTE")
        print("=" * 60 + "\n")

        try:
            print("Seleccione el tipo de cliente:")
            print("1. Regular (sistema de puntos)")
            print("2. Premium (descuentos exclusivos)")
            print("3. Corporativo (cliente empresarial)")
            tipo_cliente = input("\nTipo (1-3): ").strip()

            if tipo_cliente not in ["1", "2", "3"]:
                print("❌ Tipo de cliente no válido.")
                self.pausa()
                return

            # Datos comunes
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            telefono = input("Teléfono (+56912345678): ").strip()
            direccion = input("Dirección: ").strip()

            # Crear cliente según tipo
            if tipo_cliente == "1":
                cliente = ClienteRegular(nombre, email, telefono, direccion)

            elif tipo_cliente == "2":
                descuento = input("Descuento exclusivo (0-100, default=10): ").strip()
                descuento = float(descuento) if descuento else 10.0
                cliente = ClientePremium(nombre, email, telefono, direccion, descuento)

            else:  # tipo_cliente == '3'
                empresa = input("Nombre de empresa: ").strip()
                rut = input("RUT empresa (ej: 12.345.678-9): ").strip()
                contacto = input("Contacto principal: ").strip()
                cliente = ClienteCorporativo(
                    nombre, email, telefono, direccion, empresa, rut, contacto
                )

            self.gestor.agregar_cliente(cliente)
            print("\n✅ Cliente registrado exitosamente!")
            print("\nInformación del cliente:")
            print(cliente.mostrar_info())
            self.pausa()

        except ClienteExistenteError as e:
            print(f"\n❌ Error: {e}")
            self.pausa()
        except (
            EmailInvalidoError,
            TelefonoInvalidoError,
            RutInvalidoError,
            DatosInvalidosError,
        ) as e:
            print(f"\n❌ Error de validación: {e}")
            self.pausa()
        except ValueError as e:
            print(f"\n❌ Error: {e}")
            self.pausa()
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            self.pausa()

    # ======================== OPERACIÓN 2: BUSCAR ========================

    def buscar_cliente(self):
        """Busca un cliente por email o nombre."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("BUSCAR CLIENTE")
        print("=" * 60 + "\n")

        try:
            busqueda = input("Ingrese email o nombre a buscar: ").strip()

            if not busqueda:
                print("❌ Debe ingresar un criterio de búsqueda.")
                self.pausa()
                return

            cliente = self.gestor.buscar_cliente(busqueda)

            if cliente:
                print("\n✅ Cliente encontrado:\n")
                print(cliente.mostrar_info())

                # Si es Premium, mostrar beneficios
                if isinstance(cliente, ClientePremium):
                    print("\n" + "-" * 60)
                    print("BENEFICIOS PREMIUM:")
                    print("-" * 60)
                    print(cliente.beneficio_exclusivo())

                # Si es Corporativo, ofrecer generar factura
                if isinstance(cliente, ClienteCorporativo):
                    print("\n" + "-" * 60)
                    opcion = input(
                        "\n¿Desea generar una factura corporativa? (S/N): "
                    ).upper()
                    if opcion == "S":
                        self._generar_factura_corporativa(cliente)
            else:
                print("\n❌ No se encontró cliente con ese criterio.")

            self.pausa()

        except Exception as e:
            print(f"\n❌ Error en búsqueda: {e}")
            self.pausa()

    # ======================== OPERACIÓN 3: LISTAR ========================

    def listar_clientes(self):
        """Lista todos los clientes con paginación."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("LISTADO DE CLIENTES")
        print("=" * 60 + "\n")

        try:
            clientes = self.gestor.listar_clientes()

            if not clientes:
                print("❌ No hay clientes registrados.")
                self.pausa()
                return

            # Paginación: mostrar de 10 en 10
            items_por_pagina = 10
            total_paginas = (len(clientes) + items_por_pagina - 1) // items_por_pagina
            pagina_actual = 1

            while pagina_actual <= total_paginas:
                inicio = (pagina_actual - 1) * items_por_pagina
                fin = min(inicio + items_por_pagina, len(clientes))

                self.limpiar_pantalla()
                print("=" * 60)
                print(f"LISTADO DE CLIENTES (Página {pagina_actual}/{total_paginas})")
                print("=" * 60 + "\n")

                for i, cliente in enumerate(clientes[inicio:fin], 1):
                    num_global = inicio + i
                    print(f"\n--- Cliente {num_global} ---")
                    print(cliente.mostrar_info())

                if pagina_actual < total_paginas:
                    opcion = input(
                        "\n(S) Siguiente página, (V) Volver atrás, (Q) Salir: "
                    ).upper()
                    if opcion == "S":
                        pagina_actual += 1
                    elif opcion == "V" and pagina_actual > 1:
                        pagina_actual -= 1
                    else:
                        break
                else:
                    input("\n(Presione ENTER para volver al menú)")
                    break

        except Exception as e:
            print(f"\n❌ Error al listar clientes: {e}")
            self.pausa()

    # ======================== OPERACIÓN 4: ACTUALIZAR ========================

    def actualizar_cliente(self):
        """Actualiza datos de un cliente existente."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("ACTUALIZAR CLIENTE")
        print("=" * 60 + "\n")

        try:
            email = input("Ingrese email del cliente a actualizar: ").strip()
            cliente = self.gestor.buscar_cliente(email)

            if not cliente:
                print(f"❌ Cliente con email {email} no encontrado.")
                self.pausa()
                return

            print("\n✅ Cliente encontrado:")
            print(cliente.mostrar_info())

            print("\n" + "-" * 60)
            print("CAMPOS A ACTUALIZAR:")
            print("-" * 60)
            print("1. Nombre")
            print("2. Email")
            print("3. Teléfono")
            print("4. Dirección")

            if isinstance(cliente, ClienteRegular):
                print("5. Puntos acumulados")
                campos_adicionales = {"5": "puntos_acumulados"}
            elif isinstance(cliente, ClientePremium):
                print("5. Descuento exclusivo")
                print("6. Fecha de membresía")
                campos_adicionales = {
                    "5": "descuento_exclusivo",
                    "6": "fecha_membresia",
                }
            elif isinstance(cliente, ClienteCorporativo):
                print("5. Empresa")
                print("6. RUT empresa")
                print("7. Contacto principal")
                campos_adicionales = {
                    "5": "empresa",
                    "6": "rut_empresa",
                    "7": "contacto_principal",
                }
            else:
                campos_adicionales = {}

            opcion = input("\nSeleccione campo a actualizar: ").strip()

            campos_basicos = {
                "1": "nombre",
                "2": "email",
                "3": "telefono",
                "4": "direccion",
            }
            campos_todos = {**campos_basicos, **campos_adicionales}

            if opcion not in campos_todos:
                print("❌ Opción no válida.")
                self.pausa()
                return

            campo = campos_todos[opcion]
            nuevo_valor = input(f"Ingrese nuevo valor para {campo}: ").strip()

            nuevos_datos = {campo: nuevo_valor}
            self.gestor.actualizar_cliente(email, nuevos_datos)

            print("\n✅ Cliente actualizado exitosamente!")
            print("\nNueva información:")
            cliente_actualizado = self.gestor.buscar_cliente(email)
            if cliente_actualizado:
                print(cliente_actualizado.mostrar_info())
            self.pausa()

        except ClienteNoEncontradoError as e:
            print(f"\n❌ Error: {e}")
            self.pausa()
        except (
            EmailInvalidoError,
            TelefonoInvalidoError,
            RutInvalidoError,
            DatosInvalidosError,
        ) as e:
            print(f"\n❌ Error de validación: {e}")
            self.pausa()
        except Exception as e:
            print(f"\n❌ Error al actualizar: {e}")
            self.pausa()

    # ======================== OPERACIÓN 5: ELIMINAR ========================

    def eliminar_cliente(self):
        """Elimina un cliente con confirmación."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("ELIMINAR CLIENTE")
        print("=" * 60 + "\n")

        try:
            email = input("Ingrese email del cliente a eliminar: ").strip()
            cliente = self.gestor.buscar_cliente(email)

            if not cliente:
                print(f"❌ Cliente con email {email} no encontrado.")
                self.pausa()
                return

            print("\n⚠️  DATOS DEL CLIENTE A ELIMINAR:")
            print("-" * 60)
            print(cliente.mostrar_info())
            print("-" * 60)

            confirmacion = input(
                "\n¿Está seguro de que desea eliminar este cliente? (S/N): "
            ).upper()

            if confirmacion != "S":
                print("Operación cancelada.")
                self.pausa()
                return

            self.gestor.eliminar_cliente(email)
            print("\n✅ Cliente eliminado exitosamente!")
            self.pausa()

        except ClienteNoEncontradoError as e:
            print(f"\n❌ Error: {e}")
            self.pausa()
        except Exception as e:
            print(f"\n❌ Error al eliminar: {e}")
            self.pausa()

    # ======================== OPERACIÓN 6: EXPORTAR CSV ========================

    def exportar_csv(self):
        """Exporta clientes a archivo CSV."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("EXPORTAR CLIENTES A CSV")
        print("=" * 60 + "\n")

        try:
            self.gestor.exportar_a_csv()
            print("✅ Clientes exportados exitosamente a 'datos/clientes.csv'")
            print("\nArchivo generado con la siguiente información:")
            print("- Tipo de cliente")
            print("- Nombre")
            print("- Email")
            print("- Teléfono")
            print("- Dirección")
            print("- Campos específicos por tipo")
            self.pausa()

        except Exception as e:
            print(f"❌ Error al exportar: {e}")
            self.pausa()

    # ======================== OPERACIÓN 7: IMPORTAR CSV ========================

    def importar_csv(self):
        """Importa clientes desde archivo CSV."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("IMPORTAR CLIENTES DESDE CSV")
        print("=" * 60 + "\n")

        try:
            ruta = input(
                "Ingrese ruta del archivo CSV (default: datos/clientes_entrada.csv): "
            ).strip()
            if not ruta:
                ruta = "datos/clientes_entrada.csv"

            print(f"\nImportando desde: {ruta}")
            stats = self.gestor.importar_desde_csv(ruta)

            print("\n✅ Importación completada!")
            print(f"Total procesados: {stats['total']}")
            print(f"Importados exitosamente: {stats['exitosos']}")
            print(f"Duplicados (no importados): {stats['duplicados']}")
            print(f"Errores: {stats['errores']}")

            self.pausa()

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {ruta}")
            print("Asegúrese de que el archivo existe en la ruta especificada.")
            self.pausa()
        except Exception as e:
            print(f"❌ Error al importar: {e}")
            self.pausa()

    # ======================== OPERACIÓN 8: GENERAR REPORTE ========================

    def generar_reporte(self):
        """Genera reporte estadístico del sistema."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("GENERAR REPORTE ESTADÍSTICO")
        print("=" * 60 + "\n")

        try:
            contenido = self.gestor.generar_reporte()

            print("✅ Reporte generado exitosamente!")
            print("\nContenido del reporte:")
            print("-" * 60)
            print(contenido)
            print("-" * 60)
            print("\nEl reporte ha sido guardado en: reportes/resumen.txt")
            self.pausa()

        except Exception as e:
            print(f"❌ Error al generar reporte: {e}")
            self.pausa()

    # ======================== OPERACIÓN 9: AYUDA ========================

    def mostrar_ayuda(self):
        """Muestra ayuda del sistema."""
        self.limpiar_pantalla()
        print("=" * 60)
        print("AYUDA DEL SISTEMA")
        print("=" * 60 + "\n")

        ayuda_text = """
GESTIÓN DE CLIENTES:

1. REGISTRAR CLIENTE
   - Seleccione tipo: Regular, Premium o Corporativo
   - Ingrese datos básicos (nombre, email, teléfono, dirección)
   - Según tipo, se solicitarán datos adicionales
   - El email debe ser único y válido

2. BUSCAR CLIENTE
   - Busque por email exacto o nombre parcial
   - La búsqueda es insensible a mayúsculas/minúsculas
   - Si encuentra cliente Premium, verá sus beneficios

3. LISTAR CLIENTES
   - Visualice todos los clientes registrados
   - Los listados se muestran de 10 en 10 (paginación)
   - Navegue con S (siguiente) y V (volver)

4. ACTUALIZAR CLIENTE
   - Busque el cliente por email
   - Seleccione el campo a modificar
   - Ingrese el nuevo valor (será validado)

5. ELIMINAR CLIENTE
   - Busque el cliente por email
   - Se mostrará la información antes de eliminar
   - Confirme la eliminación (S/N)

6. EXPORTAR A CSV
   - Guarda todos los clientes en 'datos/clientes.csv'
   - Formato compatible con Excel y otras aplicaciones
   - Incluye todos los datos del cliente

7. IMPORTAR DESDE CSV
   - Lee clientes de un archivo CSV
   - Se valida cada registro antes de importar
   - Se crea automáticamente un backup
   - Ruta por default: datos/clientes_entrada.csv

8. GENERAR REPORTE
   - Crea estadísticas del sistema
   - Incluye conteos por tipo de cliente
   - Se guarda en 'reportes/resumen.txt'

TIPOS DE CLIENTES:

Regular:
  - Sistema de puntos por compras
  - Acumula puntos automaticamente
  - Puede canjear puntos

Premium:
  - Descuento exclusivo (0-100%)
  - Fecha de membresía
  - Beneficios especiales

Corporativo:
  - Información empresarial
  - RUT validado
  - Contacto principal
  - Generación de facturas

VALIDACIONES:

- Email: formato estándar (usuario@dominio.com)
- Teléfono: formato chileno (+56912345678 o 0912345678)
- RUT: formato chileno con dígito verificador (12.345.678-9)
- Campos de texto: no pueden estar vacíos
"""

        print(ayuda_text)
        self.pausa()

    # ======================== OPERACIÓN 0: SALIR ========================

    def salir(self):
        """Termina la ejecución del programa."""
        self.limpiar_pantalla()
        print("\n" + "=" * 60)
        print("¡Gracias por usar el Gestor Inteligente de Clientes!")
        print("Los cambios han sido registrados correctamente.")
        print("=" * 60 + "\n")
        self.ejecutando = False

    # ======================== MÉTODOS AUXILIARES ========================

    def _generar_factura_corporativa(self, cliente):
        """Genera una factura corporativa para un cliente."""
        try:
            print("\n" + "=" * 60)
            print("GENERAR FACTURA CORPORATIVA")
            print("=" * 60)

            numero_factura = input("\nNúmero de factura: ").strip()
            monto = input("Monto total: $").strip()
            descripcion = input("Descripción del servicio/producto: ").strip()

            monto = float(monto)
            factura = cliente.generar_factura_corporativa(
                numero_factura, monto, descripcion
            )

            print(factura)

            # Opción de guardar factura
            guardar = input("¿Desea guardar la factura en un archivo? (S/N): ").upper()
            if guardar == "S":
                nombre_archivo = f"reportes/factura_{numero_factura}.txt"
                with open(nombre_archivo, "w", encoding="utf-8") as f:
                    f.write(factura)
                print(f"✅ Factura guardada en: {nombre_archivo}")

        except ValueError:
            print("❌ Monto debe ser un número válido.")
        except Exception as e:
            print(f"❌ Error generando factura: {e}")


def main():
    """Función principal que inicia la aplicación."""
    try:
        interfaz = InterfazGIC()
        interfaz.ejecutar()
    except KeyboardInterrupt:
        print("\n\n⚠️ Aplicación interrumpida por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
