
from enum import Enum
from datetime import date, datetime
'''
  Todos los atributos son privados con doble guion bajo (__atributo) y
  se acceden/modifican solo mediante @property y @setter
'''
# definición de clase EntidadBase
class EntidadBase:
    """Clase base para todas las entidades del sistema."""
    pass

# definición de la clase Categoria
class Categoria(EntidadBase):
    """Define el rubro al que pertenece un producto (ej: 'Periféricos', 'Hardware')."""

    def __init__(self, id: int, nombre: str):
        """
        Inicializa una nueva instancia de Categoria. Constructor.

        Args:
            id (int): Identificador único positivo de la categoría.
            nombre (str): Nombre descriptivo de la categoría (ej: 'Hardware').
        """
        self.id = id
        self.nombre = nombre

    @property
    def id(self) -> int:
        """Retorna el identificador único de la categoría."""
        return self.__id

    @id.setter
    def id(self, valor: int):
        """Establece el ID de la categoría. Debe ser un entero positivo."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("id debe ser un entero positivo.")
        self.__id = valor


    @property
    def nombre(self) -> str:
        """Retorna el nombre descriptivo de la categoría."""
        return self.__nombre


    @nombre.setter
    def nombre(self, valor: str):
        """Establece el nombre de la categoría. No puede estar vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        self.__nombre = valor.strip()


    def __str__(self)->str:
       """Retorna una representación legible de la categoría."""
       return f"Categoria(id={self.__id}, nombre='{self.__nombre}')"

    def __repr__(self):
        """Retorna la representación técnica del objeto, útil para debugging."""
        return self.__str__()


# definición de la clase Proveedor

class Proveedor(EntidadBase):
    """Entidad que provee la mercadería. Registra ID, nombre legal y contacto."""

    def __init__(self, id: int, nombre: str, contacto: str):
        """
        Inicializa una nueva instancia de Proveedor. Constructor.

        Args:
            id (int): Identificador único positivo del proveedor.
            nombre (str): Nombre descriptivo del proveedor (ej: 'Nexus').
            contacto (str): mail o telefono de contacto del proveedor.
        """
        self.id = id
        self.nombre = nombre
        self.contacto = contacto

    @property
    def id(self) -> int:
        """Retorna el identificador único del proveedor."""
        return self.__id

    @id.setter
    def id(self, valor: int):
        """Establece el identificador ID del proveedor. Deber ser positivo."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("id debe ser un entero positivo.")
        self.__id = valor

    @property
    def nombre(self) -> str:
        """Retorna el nombre descriptivo del proveedor."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Establece el nombre de la proveedor. No puede estar vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del proveedor no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def contacto(self) -> str:
        """Retorna el contacto (mail/teléfono) del proveedor."""
        return self.__contacto

    @contacto.setter
    def contacto(self, valor: str):
        """Establece el contacto proveedor mail/teléfono. No puede estar vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El contacto del proveedor no puede estar vacío.")
        self.__contacto = valor.strip()

    def __str__(self)->str:
        return (f"Proveedor(id={self.__id}, "
                f"nombre='{self.__nombre}', contacto='{self.__contacto}')")

    def __repr__(self):
        return self.__str__()

# definición de la clase Moneda
class Moneda(EntidadBase):
    """
    Representa la moneda en la que esta un precio.
    """
    def __init__(self, id: int, nombre: str):
        """
        Inicializa una nueva instancia de Moneda().

        Args:
            id (int): identificador de la moneda.
            nombre (str): Nombre de la  moneda.
        """
        if not isinstance(id,int) or id <=0 or not isinstance(nombre,str):
          raise ValueError("El identificador de la moneda debe ser positivo")
        self.id = id
        self.nombre = nombre

    @property
    def id(self) -> int:
        """Retorna el identificador de la moneda."""
        return self.__id

    @property
    def nombre(self) -> str:
        """Retorna el nombre de la moneda."""
        return self.__nombre

    @id.setter
    def id(self, valor: int):
        """Establece el valor del identificador.
        Debe ser estrictamente mayor a cero."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El valor de la moneda debe ser mayor a cero.")
        self.__id = int(valor)

    @nombre.setter
    def nombre(self, nombre_moneda: str):
        """Establece el nombre de la moneda.
        No puede estar vacío."""
        if not isinstance(nombre_moneda, str) or not nombre_moneda.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre_moneda.strip()

# definición de la clase Precio
class Precio():
    """
    Representa el precio de un producto.
    Contiene el valor, la moneda en código ISO y la fecha de última actualización.
    """

    def __init__(self, valor: float, moneda: Moneda, fecha: date = None):
        """
        Inicializa una nueva instancia de Precio. Constructor

        Args:
            valor (float): Valor del precio. No puede ser negativo.
            moneda (str): Código de 3 letras de la moneda (ej: ARS, USD).
            fecha (date): Fecha de última actualización.
        """
        if valor < 0:
            raise ValueError("El valor no puede ser negativo")

        if not isinstance(moneda, Moneda):
            raise TypeError("Debe ser una moneda válida")

        self.valor = valor
        self.moneda = moneda
        self.fecha_actualizacion = fecha or date.today()


    @property
    def valor(self) -> float:
        """Retorna el valor del precio."""
        return self.__valor

    @valor.setter
    def valor(self, precio: float):
        """ Establece el valor del precio. No puede ser negativo."""
        if not isinstance(precio, (int, float)) or precio < 0:
            raise ValueError("El valor del precio no puede ser negativo.")
        self.__valor = float(precio)


    @property
    def moneda(self) -> Moneda:
        """Retorna el código de la moneda."""
        return self.__moneda

    @moneda.setter
    def moneda(self, tipo_moneda: Moneda):
        """Establece la moneda. Debe ser un código de exactamente 3 letras."""
        if not isinstance(tipo_moneda, Moneda):
            raise ValueError("La moneda debe una instancia de la clase Moneda.")
        self.__moneda = tipo_moneda


    @property
    def fecha_actualizacion(self) -> date:
        """Retorna la fecha de última actualización del precio."""
        return self.__fecha_actualizacion

    @fecha_actualizacion.setter
    def fecha_actualizacion(self, fecha:date):
        """Establece la fecha de actualización. Debe ser un objeto date."""
        if not isinstance(fecha, date):
            raise ValueError("La fecha de actualización debe ser un objeto date.")
        self.__fecha_actualizacion = fecha

    def __str__(self):
        """Retorna una representación legible del precio."""
        return (f"Precio(valor={self.__valor:.2f}, moneda='{self.__moneda}', "
                f"fecha='{self.__fecha_actualizacion}')")

    def __repr__(self):
        """Retorna la representación técnica del objeto, útil para debugging."""
        return self.__str__()

# definición de la clase TipoCotización
class TipoCotizacion(EntidadBase):
    def __init__(self, id: int, nombre: str):
        """
        Inicializa una nueva instancia de TipoCotizacion().

        Args:
            id (int): identificador del tipo de cotización.
            nombre (str): Nombre del tipo de cotización.
        """
        if not isinstance(id,int) or id <=0 or not isinstance(nombre,str):
          raise ValueError("El identificador del Tipo de cotización debe ser positivo")
        self.id=id
        self.nombre=nombre

    @property
    def id(self) -> int:
        """Retorna el identificador del tipo de Cotización."""
        return self.__id

    @property
    def nombre(self) -> str:
        """Retorna el nombre del tipo de Cotización."""
        return self.__nombre

    @id.setter
    def id(self, valor: int):
        """Establece el valor del identificador.
        Debe ser estrictamente mayor a cero."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El valor de la cotización debe ser mayor a cero.")
        self.__id = int(valor)

    @nombre.setter
    def nombre(self, nombre_tipo: str):
        """Establece el nombre del tipo de la cotización.
        No puede estar vacío."""
        if not isinstance(nombre_tipo, str) or not nombre_tipo.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nombre_tipo.strip()

    def __str__(self):
        """Retorna una representación legible del Tipo de Cotización."""
        return self.nombre

    def __repr__(self):
        """Retorna la representación técnica del objeto, útil para debugging."""
        return self.__str__()

# definición de la clase CotizacionDolar
class CotizacionDolar():
    """
    Registra la cotización diaria del dólar.
    Permite controlar el valor según el tipo de cambio del día.
    """

    def __init__(self, valor: float, fecha: date, tipo: TipoCotizacion):
        """
        Inicializa una nueva instancia de CotizacionDolar.

        Args:
            valor (float): Valor de la cotización. Debe ser mayor a cero.
            fecha (date): Fecha de la cotización.
            tipo (str): Tipo de cambio (ej: 'Oficial', 'Blue', 'Bolsa').
        """
        if valor <= 0:
            raise ValueError("La cotización debe ser positiva")

        if not isinstance(tipo, TipoCotizacion):
            raise TypeError("Tipo de cotización inválido")

        self.valor = valor
        self.fecha = fecha
        self.tipo = tipo

    @property
    def valor(self) -> float:
        """Retorna el valor de la cotización del dólar."""
        return self.__valor

    @valor.setter
    def valor(self, v: float):
        """Establece el valor de la cotización.
        Debe ser estrictamente mayor a cero."""
        if not isinstance(v, (int, float)) or v <= 0:
            raise ValueError("El valor de la cotización debe ser mayor a cero.")
        self.__valor = float(v)


    @property
    def fecha(self) -> date:
        """Retorna la fecha de la cotización."""
        return self.__fecha

    @fecha.setter
    def fecha(self, fecha: date):
        """Establece la fecha de la cotización. Debe ser un objeto date."""
        if not isinstance(fecha, date):
            raise ValueError("La fecha debe ser un objeto date.")
        self.__fecha = fecha

    @property
    def tipo(self) -> str:
        """Retorna el tipo de cambio de la cotización."""
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo_cambio: str):
        """Establece el tipo de cambio.
        """
        if not isinstance(tipo_cambio, TipoCotizacion):
            raise ValueError(f"Tipo inválido.")
        self.__tipo = tipo_cambio

    def __str__(self):
        """Retorna una representación legible de la cotización."""
        return (f"CotizacionDolar(tipo='{self.__tipo}', valor={self.__valor:.2f}, "
                f"fecha='{self.__fecha}')")

    def __repr__(self):
        """Retorna la representación técnica del objeto, útil para debugging."""
        return self.__str__()

# definición de la clase Producto
class Producto(EntidadBase):
    """
    Representa el producto central del sistema.
    Asocia un Precio, una Categoria y un Proveedor en un único objeto.
    """

    def __init__(self, id: int, nombre: str, descripcion: str,
                 precio: Precio, categoria: Categoria, proveedor: Proveedor):

        """
        Inicializa una nueva instancia de Producto.

        Args:
            id_producto (int): Identificador único positivo del producto.
            nombre (str): Nombre del producto (ej: 'SSD Samsung 1TB').
            descripcion (str): Descripción detallada del producto.
            precio (Precio): Instancia de Precio asociada al producto.
            categoria (Categoria): Instancia de Categoria a la que pertenece el producto.
            proveedor (Proveedor): Instancia de Proveedor que abastece el producto.
        """

        self.id = int(id)
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.proveedor = proveedor

    @property
    def id(self) -> int:
        """Retorna el identificador único del producto."""
        return self.__id

    @id.setter
    def id(self, valor: int):
        """Establece el ID del producto. Debe ser un entero positivo."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("id_producto debe ser un entero positivo.")
        self.__id = valor

    @property
    def nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre_producto: str):
        """Establece el nombre del producto. No puede estar vacío."""
        if not isinstance(nombre_producto, str) or not nombre_producto.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self.__nombre = nombre_producto.strip()

    @property
    def descripcion(self) -> str:
        """Retorna la descripción del producto."""
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion_producto: str):
        """Establece la descripción del producto. Debe ser texto."""
        if not isinstance(descripcion_producto, str):
            raise ValueError("La descripción debe ser texto.")
        self.__descripcion = descripcion_producto.strip()

    @property
    def precio(self) -> Precio:
        """Retorna la instancia de Precio asociada al producto."""
        return self.__precio

    @precio.setter
    def precio(self, precio_producto: Precio):
        """Establece el precio del producto. Debe ser una instancia de Precio."""
        if not isinstance(precio_producto, Precio):
            raise TypeError("El precio debe ser una instancia de Precio.")
        self.__precio = precio_producto

    @property
    def categoria(self) -> Categoria:
        """Retorna la categoría a la que pertenece el producto."""
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria_producto: Categoria):
        """Establece la categoría del producto. Debe ser una instancia de Categoria."""
        if not isinstance(categoria_producto, Categoria):
            raise TypeError("La categoría debe ser una instancia de Categoria.")
        self.__categoria = categoria_producto

    @property
    def proveedor(self) -> Proveedor:
        """Retorna el proveedor que abastece el producto."""
        return self.__proveedor

    @proveedor.setter
    def proveedor(self, proveedor_producto: Proveedor):
        """Establece el proveedor del producto. Debe ser una instancia de Proveedor."""
        if not isinstance(proveedor_producto, Proveedor):
            raise TypeError("El proveedor debe ser una instancia de Proveedor.")
        self.__proveedor = proveedor_producto

    def __str__(self):
        """Retorna una representación legible del producto."""
        return (f"Producto(id={self.__id}, nombre='{self.__nombre}', "
                f"precio={self.__precio}, categoria={self.__categoria.nombre})")

    def __repr__(self):
        """Retorna la representación técnica del objeto, útil para debugging."""
        return self.__str__()

# definición de la clase Stock
class Stock():
    """
    Vincula un Producto con un Almacén específico.
    Registra la cantidad disponible, la cual nunca puede ser menor a cero.
    """

    def __init__(self, producto: Producto, nombre_almacen: str, cantidad: int):
        """
        Inicializa una nueva instancia de Stock.

        Args:
            producto (Producto): Instancia del producto almacenado.
            almacen (str): Nombre del almacén donde se encuentra el producto.
            cantidad (int): Cantidad disponible del producto. No puede ser negativa.
        """
        self.producto = producto
        self.almacen = nombre_almacen
        self.cantidad = cantidad

    @property
    def producto(self) -> Producto:
        """Retorna el producto asociado a este stock."""
        return self.__producto

    @producto.setter
    def producto(self, producto_stock: Producto):
        """Establece el producto del stock. Debe ser una instancia de Producto."""
        if not isinstance(producto_stock, Producto):
            raise TypeError("El producto debe ser una instancia de Producto.")
        self.__producto = producto_stock

    @property
    def almacen(self) -> str:
        """Retorna el nombre del almacén donde se encuentra el producto."""
        return self.__almacen

    @almacen.setter
    def almacen(self, nombre_almacen: str):
        """Establece el nombre del almacén. No puede estar vacío."""
        if not isinstance(nombre_almacen, str) or not nombre_almacen.strip():
            raise ValueError("El nombre del almacén no puede estar vacío.")
        self.__almacen = nombre_almacen.strip()

    @property
    def cantidad(self) -> int:
        """Retorna la cantidad disponible del producto en el almacén."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad_producto: int):
        """Establece la cantidad disponible. No puede ser negativa."""
        if not isinstance(cantidad_producto, int) or cantidad_producto < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad_producto


    def __str__(self):
        """Retorna una representación legible del stock."""
        return (f"Stock(producto='{self.__producto.nombre}', "
                f"almacen='{self.__almacen}', cantidad={self.__cantidad})")

    def __repr__(self):
        """Retorna la representación técnica del objeto, útil para debugging."""
        return self.__str__()
