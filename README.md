
>>**PRICE MANAGER**

>>Sistema de Gestión de Inventario

>>Sprint_1

**Objetivo**

Desarrollar una aplicación de consola (CLI) robusta en Python que permita gestionar el inventario de un local de hardware, cotizar productos en tiempo real según el valor del dólar y comparar precios automáticamente con la competencia web.

**Introducción y contexto del sprint**

Una empresa distribuidora de productos electrónicos necesita modernizar su sistema de gestión de inventarios. Debido a la volatilidad económica del mercado argentino, el sistema debe ser capaz de gestionar precios en diferentes monedas (ARS, USD, entre otras) y realizar un seguimiento detallado de la cotización del dólar para actualizar sus valores en tiempo real.
En este primer sprint se construyó la base completa del sistema, aplicando una arquitectura en capas:

* **Capa de Entidades**: Modelado de los objetos del negocio con encapsulación estricta.
* **Capa de Repositorios**: Persistencia en memoria con interfaces CRUD bien definidas.
* **Capa de Servicios**: Lógica de negocio, validaciones y reglas del dominio.
* **Capa de UI**: Interfaz de consola interactiva con menús y submenús para todas las entidades.

>> **Estructura del proyecto**

price_manager/
>>>> src/
>>>>>price_manager/
│       ├── entities/
│       │   └── entities.py
│       ├── preload_data/
│       │   └── preload_data.py
│       ├── repositories/
│       │   └── repositories.py
│       ├── services/
│       │   └── services.py
│       ├── migrations/
│       │   └── csv/
│       │       ├── categorias.csv
│       │       ├── proveedores.csv
│       │       ├── monedas.csv
│       │       ├── tipos_cotizaciones.csv
│       │       ├── productos.csv
│       │       ├── stock.csv
│       │       └── cotizaciones_dolar.csv
│       ├── ui/
│       │   └── console.py
│       └── main.py
├── requirements.txt
├── CHANGELOG.md
└── README.md


**Cómo ejecutar la aplicación**

  Desde el notebook, ejecutando la celda de main.py con import_default_data=True.

**Entidades del sistema**

  * Entidad: *Categoria*
  ** Descripción: Rubro del producto (ej: Hardware, Periféricos)

  Entidad: *Proveedor*
  Descripción: Empresa que abastece los productos

  Entidad: *Moneda*
  Descripción: Moneda en la que se expresa un precio

  Entidad: *Precio*
  Descripción: PrecioValor + moneda + fecha de actualización

  Entidad: *TipoCotizacion*
  Descripción: Tipo de cambio (Oficial, Blue, Bolsa, etc.)

  Entidad:*CotizacionDolar*
  Descripción: Valor diario del dólar por tipo

  Entidad: *Producto*
  Descripción: Unidad central del sistema

  Entidad: *Stock*
  Descripción: Cantidad disponible de un producto en un almacén
