# Diagrama de Clases UML - Gestor Inteligente de Clientes (GIC)

## Diagrama Completo en Mermaid

```mermaid
classDiagram
    class Cliente {
        -__nombre: str
        -__email: str
        -__telefono: str
        -__direccion: str
        +__init__(nombre: str, email: str, telefono: str, direccion: str)
        +get_nombre() str
        +set_nombre(valor: str) None
        +get_email() str
        +set_email(valor: str) None
        +get_telefono() str
        +set_telefono(valor: str) None
        +get_direccion() str
        +set_direccion(valor: str) None
        +mostrar_info() str*
        +__str__() str
        +__repr__() str
        +to_dict() dict
    }

    class ClienteRegular {
        -__puntos_acumulados: int
        +__init__(nombre: str, email: str, telefono: str, direccion: str, puntos: int)
        +get_puntos_acumulados() int
        +set_puntos_acumulados(valor: int) None
        +acumular_puntos(cantidad: int) None
        +mostrar_info() str
        +to_dict() dict
    }

    class ClientePremium {
        -__descuento_exclusivo: float
        -__fecha_membresia: str
        +__init__(nombre: str, email: str, telefono: str, direccion: str, descuento: float, fecha: str)
        +get_descuento_exclusivo() float
        +set_descuento_exclusivo(valor: float) None
        +get_fecha_membresia() str
        +set_fecha_membresia(valor: str) None
        +beneficio_exclusivo() str
        +mostrar_info() str
        +to_dict() dict
    }

    class ClienteCorporativo {
        -__empresa: str
        -__rut_empresa: str
        -__contacto_principal: str
        +__init__(nombre: str, email: str, telefono: str, direccion: str, empresa: str, rut: str, contacto: str)
        +get_empresa() str
        +set_empresa(valor: str) None
        +get_rut_empresa() str
        +set_rut_empresa(valor: str) None
        +get_contacto_principal() str
        +set_contacto_principal(valor: str) None
        +generar_factura_corporativa(numero: str, monto: float, descripcion: str) str
        +mostrar_info() str
        +to_dict() dict
    }

    class GestorClientes {
        -__clientes: list[Cliente]
        -__ruta_csv: str
        -__ruta_log: str
        -__logger: Logger
        +__init__(ruta_csv: str, ruta_log: str)
        +agregar_cliente(cliente: Cliente) None
        +buscar_cliente(criterio: str) Cliente|None
        +listar_clientes() list[Cliente]
        +actualizar_cliente(email: str, datos: dict) None
        +eliminar_cliente(email: str) None
        +exportar_a_csv() None
        +importar_desde_csv(ruta: str) dict
        +generar_reporte() str
        +registrar_actividad(accion: str, mensaje: str) None
        -__validar_email_unico(email: str) bool
        -__configurar_logger() None
    }

    class Validaciones {
        +validar_email(email: str)$ bool
        +validar_telefono(telefono: str)$ bool
        +validar_rut(rut: str)$ bool
        +validar_texto_no_vacio(texto: str, campo: str)$ bool
        -__calcular_digito_verificador(rut_sin_dv: str)$ str
    }

    class Excepciones {
        <<abstract>>
    }

    class EmailInvalidoError {
        +__init__(mensaje: str)
    }

    class TelefonoInvalidoError {
        +__init__(mensaje: str)
    }

    class ClienteExistenteError {
        +__init__(mensaje: str)
    }

    class ClienteNoEncontradoError {
        +__init__(mensaje: str)
    }

    class DatosInvalidosError {
        +__init__(mensaje: str)
    }

    class RutInvalidoError {
        +__init__(mensaje: str)
    }

    %% Relaciones de Herencia
    Cliente <|-- ClienteRegular
    Cliente <|-- ClientePremium
    Cliente <|-- ClienteCorporativo

    %% Relaciones de Composición
    GestorClientes o-- "0..*" Cliente : gestiona

    %% Relaciones de Dependencia
    GestorClientes --> Validaciones : utiliza
    GestorClientes --> Excepciones : lanza
    ClienteRegular --> Excepciones : lanza
    ClientePremium --> Excepciones : lanza
    ClienteCorporativo --> Excepciones : lanza

    %% Herencia de Excepciones
    Exception <|-- Excepciones
    Excepciones <|-- EmailInvalidoError
    Excepciones <|-- TelefonoInvalidoError
    Excepciones <|-- ClienteExistenteError
    Excepciones <|-- ClienteNoEncontradoError
    Excepciones <|-- DatosInvalidosError
    Excepciones <|-- RutInvalidoError
