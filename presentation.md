# Gestor Inteligente de Clientes (GIC)

## Presentación del Proyecto

---

## Descripción del Proyecto

El **Gestor Inteligente de Clientes (GIC)** es una aplicación de gestión empresarial desarrollada en Python que permite administrar diferentes tipos de clientes (regulares, premium y corporativos) con funcionalidades completas de CRUD, importación/exportación de datos, validación robusta y generación de reportes.

---

## Objetivos Alcanzados

✅ **Implementación de Programación Orientada a Objetos (POO)**

- Herencia: Clase base `Cliente` con tres subclases especializadas
- Polimorfismo: Métodos sobrescritos en cada subclase
- Encapsulación: Atributos privados con propiedades (properties)
- Abstracción: Métodos abstractos en la clase base

✅ **Gestión de Datos Completa**

- Operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
- Persistencia mediante archivos CSV
- Importación y exportación de datos
- Almacenamiento en memoria durante la sesión

✅ **Sistema de Validación Robusto**

- 6 funciones de validación con expresiones regulares
- Validación de email, teléfono, RUT, nombre y categoría
- Mensajes de error específicos y útiles

✅ **Manejo de Excepciones Personalizado**

- 6 excepciones personalizadas para diferentes escenarios
- Control de errores en operaciones críticas
- Recuperación elegante ante fallos

✅ **Sistema de Logging**

- Registro automático de todas las operaciones
- Trazabilidad completa del programa
- Información de debugging y auditoría

✅ **Interfaz de Usuario Intuitiva**

- Menú interactivo con 10 opciones
- Carga automática de datos de prueba
- Validación en tiempo real
- Mensajes claros y contextuales

---

## Tecnologías Utilizadas

- **Lenguaje**: Python 3.7+
- **Paradigma**: Programación Orientada a Objetos
- **Módulos Estándar**:
  - `csv` - Manejo de archivos de datos
  - `logging` - Sistema de registro de operaciones
  - `os` - Operaciones del sistema operativo
  - `shutil` - Utilidades de archivos
  - `datetime` - Gestión de fechas y horas

---

## Componentes del Sistema

### Módulos Implementados

| Módulo                   | Responsabilidad                       | Líneas |
| ------------------------ | ------------------------------------- | ------ |
| `cliente.py`             | Clase base con validaciones iniciales | 85     |
| `cliente_regular.py`     | Subclase con descuentos por categoría | 45     |
| `cliente_premium.py`     | Subclase con beneficios VIP           | 35     |
| `cliente_corporativo.py` | Subclase con datos corporativos       | 50     |
| `gestor_clientes.py`     | Gestor central CRUD y persistencia    | 529    |
| `validaciones.py`        | Funciones de validación con regex     | 120    |
| `excepciones.py`         | 6 excepciones personalizadas          | 35     |
| `main.py`                | Interfaz interactiva del usuario      | 650    |

**Total**: ~1,550 líneas de código bien estructurado y documentado

### Arquitectura

```
┌─────────────────────────────────────┐
│    InterfazGIC (main.py)            │
│    - Menú interactivo               │
│    - Gestión de entrada/salida      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    GestorClientes                   │
│    - CRUD operations                │
│    - Persistencia CSV               │
│    - Logging                        │
│    - Reportes                       │
└──────────────┬──────────────────────┘
               │
     ┌─────────┼─────────┐
     │         │         │
┌────▼──┐ ┌───▼───┐ ┌───▼────────┐
│Regular│ │Premium│ │Corporativo │
└───────┘ └───────┘ └────────────┘
     │         │         │
     └─────────┴─────────┘
            │
     ┌──────▼───────┐
     │Cliente (Base)│
     └──────────────┘
```

---

## Funcionalidades Implementadas

### 1. Gestión de Clientes Segmentados

**Cliente Regular**

- Descuento por categoría de compra (A: 5%, B: 10%, C: 15%)
- Información de categoría de cliente

**Cliente Premium**

- Descuento fijo del 20%
- Beneficio exclusivo: "Acceso VIP a eventos corporativos"
- Soporte prioritario

**Cliente Corporativo**

- RUT corporativo con validación especial
- Información de industria/sector
- Descuento personalizado según monto
- Facturación corporativa automática

### 2. Operaciones Disponibles

| #   | Operación    | Descripción                                   |
| --- | ------------ | --------------------------------------------- |
| 1   | Registrar    | Agregar nuevo cliente con validación completa |
| 2   | Buscar       | Búsqueda por email o nombre                   |
| 3   | Listar       | Mostrar todos los clientes registrados        |
| 4   | Actualizar   | Modificar datos de cliente existente          |
| 5   | Eliminar     | Remover cliente del sistema                   |
| 6   | Exportar CSV | Guardar clientes en archivo CSV               |
| 7   | Importar CSV | Cargar clientes desde archivo CSV             |
| 8   | Reporte      | Generar estadísticas de clientes              |
| 9   | Ayuda        | Mostrar información de uso                    |
| 0   | Salir        | Cerrar la aplicación                          |

### 3. Validaciones Implementadas

- **Email**: Formato RFC 5322 (usuario@dominio.com)
- **Teléfono**: Exactamente 9 dígitos numéricos
- **RUT**: Formato XX.XXX.XXX-K con validación de dígito verificador
- **Nombre**: Entre 3 y 50 caracteres
- **Categoría Premium**: Validación de etiqueta especial
- **RUT Corporativo**: Formato específico para empresas

### 4. Persistencia de Datos

- **Almacenamiento**: Archivos CSV en la carpeta `datos/`
- **Carga Automática**: Al iniciar, importa `clientes_entrada.csv` automáticamente
- **Exportación**: Genera reportes y backups en CSV
- **Integridad**: Validación de duplicados antes de importar

### 5. Logging y Auditoría

Todas las operaciones se registran en `logs/app.log`:

- Clientes creados, actualizados o eliminados
- Importaciones y exportaciones de datos
- Errores y excepciones
- Accesos y búsquedas
- Timestamps de cada operación

---

## Requisitos de Evaluación Cumplidos

✅ **Uso de Clases y Herencia**

- Clase base `Cliente` con subclases para Regular, Premium y Corporativo
- Métodos sobrescritos (`mostrar_info()`, `calcular_descuento()`)

✅ **Encapsulación**

- Atributos privados (con `__` prefix)
- Acceso mediante properties y métodos públicos
- Validación en setters

✅ **Polimorfismo**

- Métodos genéricos que se comportan diferente según el tipo
- Interfaz uniforme para diferentes tipos de clientes

✅ **Manejo de Excepciones**

- 6 excepciones personalizadas
- Try-except en operaciones críticas
- Mensajes de error contextuales

✅ **Validación de Datos**

- Expresiones regulares para validación
- Funciones dedicadas de validación
- Mensajes específicos para cada error

✅ **Entrada/Salida**

- Lectura/escritura de archivos CSV
- Interfaz de consola interactiva
- Logging a archivo

✅ **Documentación**

- Docstrings en todas las clases y métodos
- Comentarios explicativos
- Documentación técnica (README.md)

---

## Flujo de Operación

```
Inicio del Programa
         ↓
  Carga automática de datos (clientes_entrada.csv)
         ↓
  Presentación del menú principal
         ↓
  Usuario selecciona opción
         ↓
  ┌──────────────────────────────────┐
  │ Validación de entrada            │
  │ Procesamiento de operación       │
  │ Interacción con GestorClientes   │
  │ Logging de operación             │
  │ Presentación de resultados       │
  └──────────────────────────────────┘
         ↓
  Retorno al menú (bucle)
         ↓
  Usuario selecciona salir (opción 0)
         ↓
  Finalización del programa
```

---

## Datos de Prueba Incluidos

El archivo `datos/clientes_entrada.csv` contiene 7 registros de prueba:

- **2 Clientes Regulares** (Juan Pérez categoría A, Pedro García categoría B)
- **2 Clientes Premium** (María López, Ana Martínez)
- **2 Clientes Corporativos** (TechCorp, Global Solutions)
- **1 Cliente Regular** (Luis Rodríguez)

Estos datos permiten demostrar todas las funcionalidades del sistema.

---

## Puntos Destacados

### Robustez

- Validación en cada punto de entrada
- Manejo de excepciones previsto
- Recuperación ante errores

### Extensibilidad

- Arquitectura permite agregar nuevos tipos de cliente fácilmente
- Módulos desacoplados y reutilizables
- Fácil integración con bases de datos en el futuro

### Usabilidad

- Interfaz clara e intuitiva
- Mensajes de error descriptivos
- Carga automática de datos
- Validación en tiempo real

### Mantenibilidad

- Código bien estructurado y documentado
- Logging completo para auditoría
- Nombres significativos en variables y funciones
- Separación de responsabilidades

---

## Conclusión

El Gestor Inteligente de Clientes (GIC) demuestra una implementación completa de conceptos de Programación Orientada a Objetos en Python, incluyendo herencia, polimorfismo, encapsulación, manejo de excepciones, validación de datos y persistencia. El sistema es funcional, robusto y está listo para uso en entornos educativos y como base para aplicaciones más complejas.
