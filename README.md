# Gestor Inteligente de Clientes (GIC)

## Descripción General

El **Gestor Inteligente de Clientes (GIC)** es un sistema de gestión de clientes desarrollado en Python con arquitectura orientada a objetos. Permite a las empresas registrar, buscar, actualizar y gestionar información de clientes de diferentes categorías (regulares, premium y corporativos), con funcionalidades avanzadas como importación/exportación de datos, generación de reportes y logging automático.

## Características Principales

- **Gestión de Clientes Segmentados**: Registro de tres tipos de clientes con características específicas
  - Clientes Regulares
  - Clientes Premium
  - Clientes Corporativos

- **Operaciones CRUD Completas**: Crear, leer, actualizar y eliminar clientes
- **Importación/Exportación de Datos**: Manejo de archivos CSV para carga y descarga de información
- **Validación Robusta**: Validación de email, teléfono, RUT mediante expresiones regulares
- **Manejo de Excepciones Personalizado**: Sistema de errores específicos para cada tipo de fallo
- **Sistema de Logging**: Registro automático de todas las operaciones del sistema
- **Generación de Reportes**: Estadísticas de clientes y análisis por categoría
- **Interfaz Interactiva**: Menú de consola intuitivo y fácil de usar

## Estructura del Proyecto

```
proyecto_gic/
├── main.py                      # Interfaz principal y menú interactivo
├── modulos/                     # Paquete con módulos del sistema
│   ├── __init__.py             # Inicializador del paquete
│   ├── cliente.py              # Clase base Cliente
│   ├── cliente_regular.py      # Subclase Cliente Regular
│   ├── cliente_premium.py      # Subclase Cliente Premium
│   ├── cliente_corporativo.py  # Subclase Cliente Corporativo
│   ├── gestor_clientes.py      # Gestor central de operaciones
│   ├── validaciones.py         # Funciones de validación
│   └── excepciones.py          # Excepciones personalizadas
├── datos/                       # Directorio de datos
│   └── clientes_entrada.csv    # Archivo de datos de prueba
├── logs/                        # Directorio de registros
│   └── app.log                 # Archivo de log del sistema
├── reportes/                    # Directorio de reportes
│   └── resumen.txt             # Resumen de operaciones
├── DIAGRAMA_UML.md             # Diagrama de arquitectura
└── README.md                    # Esta documentación
```

## Requisitos del Sistema

- **Python**: 3.7 o superior
- **Librerías Estándar**: El sistema solo utiliza módulos estándar de Python
  - `csv`: Manejo de archivos CSV
  - `logging`: Sistema de logging
  - `os`: Operaciones del sistema operativo
  - `shutil`: Operaciones de archivos
  - `datetime`: Manejo de fechas

## Instalación y Configuración

### Paso 1: Clonar o descargar el proyecto

```bash
# Descargar el archivo del proyecto
# Extraer en el directorio deseado
```

### Paso 2: Verificar estructura de directorios

Asegúrese de que existan los directorios necesarios:

```bash
# En Windows PowerShell
mkdir -Force datos, logs, reportes
```

### Paso 3: Preparar datos de prueba

El archivo `datos/clientes_entrada.csv` debe estar en la raíz del directorio `datos/`:

```
tipo_cliente,nombre,email,telefono,rut,categoria
Regular,Juan Pérez,juan@gmail.com,987654321,12345678-9,A
Regular,Pedro García,pedro@gmail.com,987654322,22345678-0,B
Premium,María López,maria@gmail.com,987654323,32345678-1,Premium
Premium,Ana Martínez,ana@gmail.com,987654324,42345678-2,Premium
Corporativo,TechCorp,contacto@techcorp.com,987654325,55666777-K,Grande
Corporativo,Global Solutions,info@global.com,987654326,66777888-L,Mediana
Regular,Luis Rodríguez,luis@gmail.com,987654327,77888999-2,A
```

## Cómo Usar

### Iniciar el Programa

```bash
python main.py
```

Al iniciar, el sistema cargará automáticamente los datos de prueba desde `datos/clientes_entrada.csv` si el archivo existe.

### Menú Principal

El programa presenta 10 opciones:

| Opción | Descripción                       |
| ------ | --------------------------------- |
| 1      | Registrar nuevo cliente           |
| 2      | Buscar cliente por email o nombre |
| 3      | Listar todos los clientes         |
| 4      | Actualizar datos de cliente       |
| 5      | Eliminar cliente                  |
| 6      | Exportar clientes a CSV           |
| 7      | Importar clientes desde CSV       |
| 8      | Generar reporte estadístico       |
| 9      | Ver ayuda                         |
| 0      | Salir del programa                |

### Ejemplos de Uso

#### Registrar un cliente nuevo

1. Seleccione opción `1`
2. Ingrese el tipo: `Regular`, `Premium` o `Corporativo`
3. Complete los datos solicitados
4. El sistema validará automáticamente email, teléfono y RUT

#### Listar todos los clientes

1. Seleccione opción `3`
2. El sistema mostrará todos los clientes registrados con sus datos

#### Generar reporte

1. Seleccione opción `8`
2. El sistema genera estadísticas de clientes por categoría

#### Exportar datos

1. Seleccione opción `6`
2. Especifique la ruta del archivo de salida
3. Los datos se guardarán en formato CSV

## Arquitectura Técnica

### Diagrama de Clases

El sistema utiliza **herencia y polimorfismo** con la siguiente estructura:

```
Cliente (Clase Base)
├── ClienteRegular
├── ClientePremium
└── ClienteCorporativo

GestorClientes (Gestor Central)
└── [Maneja CRUD y persistencia]

Validaciones (Módulo Utilitario)
└── [Funciones de validación]

Excepciones (Sistema de Errores)
└── [6 excepciones personalizadas]
```

### Clases Principales

#### Cliente (Clase Base)

```python
class Cliente:
    - __nombre (private)
    - __email (private)
    - __telefono (private)
    - __rut (private)
    - __fecha_registro (private)

    Métodos:
    + nombre (property)
    + email (property)
    + telefono (property)
    + rut (property)
    + mostrar_info() (abstract)
```

#### Subclases

- **ClienteRegular**: Descuentos basados en categoría (A, B, C)
- **ClientePremium**: Beneficios exclusivos y soporte prioritario
- **ClienteCorporativo**: RUT corporativo, industria, facturación

#### GestorClientes

Maneja:

- Almacenamiento en memoria (\_\_clientes list)
- CRUD operations
- Importación/exportación CSV
- Logging de operaciones
- Generación de reportes

### Validaciones Implementadas

| Validación        | Patrón                | Ejemplo             |
| ----------------- | --------------------- | ------------------- |
| Email             | RFC 5322 simplificado | usuario@dominio.com |
| Teléfono          | 9 dígitos numéricos   | 987654321           |
| RUT               | Formato XX.XXX.XXX-K  | 12.345.678-9        |
| Nombre            | 3-50 caracteres       | Juan Pérez          |
| Categoría Premium | Premium               | Premium             |
| RUT Corporativo   | Formato corporativo   | 55.666.777-K        |

### Excepciones Personalizadas

El sistema implementa 6 excepciones específicas:

1. **ClienteExistenteError**: Cliente ya registrado
2. **ClienteNoEncontradoError**: Cliente no existe
3. **EmailInvalidoError**: Email no válido
4. **TelefonoInvalidoError**: Teléfono no válido
5. **RutInvalidoError**: RUT no válido
6. **DatosInvalidosError**: Datos generales inválidos

### Sistema de Logging

Todos los eventos se registran en `logs/app.log`:

- Clientes agregados/eliminados
- Operaciones de importación/exportación
- Errores y excepciones
- Búsquedas y actualizaciones

Formato: `[TIMESTAMP] - NIVEL - MENSAJE`

## Flujo de Datos

```
Inicio del Programa
    ↓
Carga automática CSV (clientes_entrada.csv)
    ↓
Menú Interactivo
    ├── Opción: Agregar → Validación → GestorClientes → Almacenamiento
    ├── Opción: Buscar → GestorClientes → Búsqueda → Mostrar
    ├── Opción: Listar → GestorClientes → Iterar → Mostrar todos
    ├── Opción: Actualizar → Búsqueda → Actualización → Almacenamiento
    ├── Opción: Eliminar → Búsqueda → Eliminación → Almacenamiento
    ├── Opción: Exportar → GestorClientes → CSV → Disco
    └── Opción: Importar → CSV → Lectura → GestorClientes → Almacenamiento
    ↓
Logging de todas las operaciones
    ↓
Salida del Programa
```

## Funcionalidades Avanzadas

### Beneficios por Tipo de Cliente

#### Cliente Regular

- Descuento por categoría (A: 5%, B: 10%, C: 15%)
- Soporte estándar
- Reportes básicos

#### Cliente Premium

- Descuento fijo: 20%
- Soporte prioritario
- Acceso a reportes avanzados
- Beneficio exclusivo: "Acceso VIP a eventos corporativos"

#### Cliente Corporativo

- Descuento personalizado según monto
- Facturación corporativa automática
- Gestor de cuenta dedicado
- Reportes personalizados por industria

### Generación de Reportes

El sistema genera reportes que incluyen:

- Total de clientes por categoría
- Descuentos promedio
- Distribución por tipo
- Estadísticas de beneficios

## Mantenimiento

### Archivo de Log

El archivo `logs/app.log` crece con cada operación. Se recomienda:

- Revisar periódicamente para errores
- Hacer backup antes de limpiar
- Usar para auditoría de operaciones

### Datos de Prueba

Para reestablecer datos de prueba:

1. Elimine el archivo `datos/clientes.csv` (si existe)
2. Reinicie el programa
3. El sistema cargará automáticamente `datos/clientes_entrada.csv`

### Respaldo de Datos

Realice backups regulares de:

- `datos/clientes.csv` (datos en producción)
- `logs/app.log` (registro de operaciones)

## Solución de Problemas

### "No hay clientes registrados" al listar

**Solución**: Los datos se cargan automáticamente. Si no aparecen, use opción 7 para importar `datos/clientes_entrada.csv`

### Error de validación al registrar cliente

**Verificar**:

- Email: Debe tener formato válido (ej: usuario@dominio.com)
- Teléfono: Debe tener 9 dígitos
- RUT: Debe tener formato XX.XXX.XXX-K

### Archivo CSV no se importa

**Verificar**:

- El archivo existe en la ruta especificada
- El formato es correcto (columnas: tipo_cliente, nombre, email, telefono, rut, categoria)
- Los datos están separados por comas

## Contribuciones y Mejoras Futuras

El sistema está diseñado para ser extensible. Posibles mejoras:

- Base de datos relacional en lugar de CSV
- API REST para integración
- Interfaz gráfica (GUI)
- Autenticación y autorización
- Exportación a otros formatos (Excel, PDF)
- Dashboard de reportes en tiempo real

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y comercial.

## Soporte

Para preguntas o problemas, revise:

1. La sección de "Solución de Problemas" en esta documentación
2. El archivo de log en `logs/app.log`
3. El diagrama UML en `DIAGRAMA_UML.md`
