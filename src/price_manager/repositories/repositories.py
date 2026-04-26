
# ------------ Interfaces
import abc
from datetime import date, datetime
from typing import TypeVar, Generic, List, Optional
from price_manager.entities.entities import EntidadBase, Categoria, Proveedor, Producto, Stock,  CotizacionDolar, Precio, Moneda, TipoCotizacion


T = TypeVar('T', bound=EntidadBase)

class IRepositorio(abc.ABC, Generic[T]):
  """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

  @abc.abstractmethod
  def crear(self, entidad: T) -> T:
    """Crea una nueva entidad en el repositorio.

    Args:
        entidad (T): La entidad a crear.

    Returns:
        T: La entidad creada.

    Raises:
        ValueError: Si ya existe una entidad con el mismo ID.
    """
    pass

  @abc.abstractmethod
  def leer_por_id(self, id: int) -> Optional[T]:
    """Lee una entidad del repositorio por su ID.

    Args:
        id (int): El ID de la entidad a leer.

    Returns:
        Optional[T]: La entidad si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def leer_todos(self) -> List[T]:
    """Lee todas las entidades del repositorio.

    Returns:
        List[T]: Una lista de todas las entidades.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, entidad: T) -> T:
    """Actualiza una entidad existente en el repositorio.

    Args:
        entidad (T): La entidad a actualizar (debe tener un ID existente).

    Returns:
        T: La entidad actualizada.

    Raises:
        ValueError: Si no se encuentra la entidad para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, id: int) -> bool:
    """Elimina una entidad del repositorio por su ID.

    Args:
        id (int): El ID de la entidad a eliminar.

    Returns:
        bool: True si la entidad fue eliminada, False si no se encontró.
    """
    pass


class IRepositorioStock(abc.ABC):
  """Interfaz para repositorios del tipo Stock."""

  @abc.abstractmethod
  def crear(self, stock: Stock) -> Stock:
    """Crea un nuevo registro de stock.

    Args:
        stock (Stock): El objeto Stock a crear.

    Returns:
        Stock: El objeto Stock creado.

    Raises:
        ValueError: Si ya existe un registro de stock para el mismo producto.
    """
    pass

  @abc.abstractmethod
  def leer_por_producto(self, producto_id: int) -> Optional['Stock']:
    """Lee un registro de stock por ID de producto.

    Args:
        producto_id (int): El ID del producto asociado al stock.

    Returns:
        Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, stock: 'Stock') -> 'Stock':
    """Actualiza un registro de stock existente.

    Args:
        stock (Stock): El objeto Stock a actualizar (debe tener un producto_id existente).

    Returns:
        Stock: El objeto Stock actualizado.

    Raises:
        ValueError: Si no se encuentra el stock para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, producto_id: int) -> bool:
    """Elimina un registro de stock por ID de producto.

    Args:
        producto_id (int): El ID del producto asociado al stock a eliminar.

    Returns:
        bool: True si el stock fue eliminado, False si no se encontró.
    """
    pass


class IRepositorioCotizacionDolar(abc.ABC):
  """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

  @abc.abstractmethod
  def crear(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
    """Crea una nueva cotización de dólar.

    Args:
        cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

    Returns:
        CotizacionDolar: El objeto CotizacionDolar creado.

    Raises:
        ValueError: Si ya existe una cotización para el mismo tipo y fecha.
    """
    pass

  @abc.abstractmethod
  def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: datetime.date) -> Optional['CotizacionDolar']:
    """Lee una cotización de dólar por tipo y fecha.

    Args:
        tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
        fecha (datetime.date): La fecha de la cotización.

    Returns:
        Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
    """
    pass

  @abc.abstractmethod
  def leer_historico_por_tipo(self, tipo_id: int) -> List['CotizacionDolar']:
    """Lee el histórico de cotizaciones para un tipo específico.

    Args:
        tipo_id (int): El ID del tipo de cotización.

    Returns:
        List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
    """
    pass

  @abc.abstractmethod
  def actualizar(self, cotizacion: 'CotizacionDolar') -> 'CotizacionDolar':
    """Actualiza una cotización de dólar existente.

    Args:
        cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

    Returns:
        CotizacionDolar: El objeto CotizacionDolar actualizado.

    Raises:
        ValueError: Si no se encuentra la cotización para actualizar.
    """
    pass

  @abc.abstractmethod
  def eliminar(self, tipo_id: int, fecha: datetime.date) -> bool:
    """Elimina una cotización de dólar por tipo y fecha.

    Args:
        tipo_id (int): El ID del tipo de cotización.
        fecha (datetime.date): La fecha de la cotización a eliminar.

    Returns:
        bool: True si la cotización fue eliminada, False si no se encontró.
    """
    pass

class RepositorioCategoria(IRepositorio[Categoria]):
    """Repositorio que gestiona las operaciones CRUD de Categoria en memoria."""

    def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__categorias = {}  # { id: Categoria }

    def crear(self, entidad: Categoria) -> Categoria:
        """Crea una nueva categoría en el repositorio."""
        if entidad.id in self.__categorias:
            raise ValueError("Ya existe una categoría con ese ID.")
        self.__categorias[entidad.id] = entidad
        return entidad

    def leer_por_id(self, id: int) -> Optional[Categoria]:
        """Retorna la categoría con el ID indicado, o None si no existe."""
        return self.__categorias.get(id, None)

    def leer_todos(self) -> List[Categoria]:
        """Retorna una lista con todas las categorías almacenadas."""
        return list(self.__categorias.values())

    def actualizar(self, entidad: Categoria) -> Categoria:
        """Actualiza una categoría existente. Lanza error si no existe."""
        if entidad.id not in self.__categorias:
            raise ValueError("Categoría no encontrada.")
        self.__categorias[entidad.id] = entidad
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina la categoría con el ID indicado. Retorna True si se eliminó."""
        if id not in self.__categorias:
            return False
        del self.__categorias[id]
        return True

class RepositorioProveedor(IRepositorio[Proveedor]):
    """Repositorio que gestiona las operaciones CRUD de Proveedor en memoria."""

    def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__proveedores = {}  # { id: Proveedor }

    def crear(self, entidad: Proveedor) -> Proveedor:
        """Crea un nuevo proveedor en el repositorio."""
        if entidad.id in self.__proveedores:
            raise ValueError("Ya existe un proveedor con ese ID.")
        self.__proveedores[entidad.id] = entidad
        return entidad

    def leer_por_id(self, id: int) -> Optional[Proveedor]:
        """Retorna el proveedor con el ID indicado, o None si no existe."""
        return self.__proveedores.get(id, None)

    def leer_todos(self) -> List[Proveedor]:
        """Retorna una lista con todos los proveedores almacenados."""
        return list(self.__proveedores.values())

    def actualizar(self, entidad: Proveedor) -> Proveedor:
        """Actualiza un proveedor existente. Lanza error si no existe."""
        if entidad.id not in self.__proveedores:
            raise ValueError("Proveedor no encontrada.")
        self.__proveedores[entidad.id] = entidad
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina el proveedor con el ID indicado. Retorna True si se eliminó."""
        if id not in self.__proveedores:
            return False
        del self.__proveedores[id]
        return True


class RepositorioProducto(IRepositorio[Producto]):
    """Repositorio que gestiona las operaciones CRUD de los productos en memoria."""

    def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__productos = {}  # { id: Producto }

    def crear(self, entidad: Producto) -> Producto:
        """Crea un nuevo producto en el repositorio."""
        if entidad.id in self.__productos:
            raise ValueError("Ya existe un producto con ese ID.")
        self.__productos[entidad.id] = entidad
        return entidad

    def leer_por_id(self, id: int) -> Optional[Producto]:
        """Retorna el producto con el ID indicado, o None si no existe."""
        return self.__productos.get(id, None)

    def leer_todos(self) -> List[Producto]:
        """Retorna una lista con todos los productos."""
        return list(self.__productos.values())

    def actualizar(self, entidad: Producto) -> Producto:
        """Actualiza un producto existente. Lanza error si no existe."""
        if entidad.id not in self.__productos:
            raise ValueError("Producto no encontrado.")
        self.__productos[entidad.id] = entidad
        return entidad

    def eliminar(self, id: int) -> bool:
        """Elimina el producto con el ID indicado. Retorna True si se eliminó."""
        if id not in self.__productos:
            return False
        del self.__productos[id]
        return True

class RepositorioStock(IRepositorioStock):
  """Repositorios del tipo Stock."""

  def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__stocks = {}  # { id: Stocks }


  def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo stock en el repositorio."""
        if stock.producto.id in self.__stocks:
            raise ValueError("Ya existe un stock con ese ID.")
        self.__stocks[stock.producto.id] = stock
        return stock


  def leer_por_producto(self, producto_id: int) -> Optional[Stock]:
        """Retorna el stock del producto indicado, o None si no existe."""
        return self.__stocks.get(producto_id, None)

  def actualizar(self, stock: Stock) -> Stock:
        """Actualiza un registro de stock existente. Lanza error si no existe."""
        if stock.producto.id not in self.__stocks:
            raise ValueError("Stock no encontrado.")
        self.__stocks[stock.producto.id] = stock
        return stock

  def eliminar(self, producto_id: int) -> bool:
        """Elimina el stock del producto indicado. Retorna True si se eliminó."""
        if producto_id not in self.__stocks:
            return False
        del self.__stocks[producto_id]
        return True

class RepositorioMoneda(IRepositorio[Moneda]):
    """Repositorio del tipo Moneda."""

    def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__moneda = {}  # { id: Moneda }

    def crear(self, tipo:Moneda)->Moneda:
      """Crea una nueva moneda en el repositorio."""
      if tipo.id in self.__moneda:
        raise ValueError("Ya existe una moneda con ese ID.")
      self.__moneda[tipo.id] = tipo
      return tipo

    def leer_por_id(self, id: int) -> Optional[Moneda]:
      """Retorna la categoría con el ID indicado, o None si no existe."""
      return self.__moneda.get(id, None)

    def leer_todos(self) -> List[Moneda]:
        return list(self.__moneda.values())

    def actualizar(self, entidad: Moneda) -> Moneda:
      """Actualiza una moneda existente. Lanza error si no existe."""
      if entidad.id not in self.__moneda:
          raise ValueError("Moneda no encontrada.")
      self.__moneda[entidad.id] = entidad
      return entidad

    def eliminar(self, id: int) -> bool:
      """Elimina la moneda con el ID indicado. Retorna True si se eliminó."""
      if id not in self.__moneda:
          return False
      del self.__moneda[id]
      return True


class RepositorioTipoCotizacion(IRepositorio[TipoCotizacion]):
    """Repositorio del tipo de cotización."""

    def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__tipocotizaciones = {}  # { id: TipoCotizaciones }

    def crear(self, tipo:TipoCotizacion)->TipoCotizacion:
      """Crea un nuevo Tipo de Cotización en el repositorio."""
      if tipo.id in self.__tipocotizaciones:
            raise ValueError("Ya existe un tipo de cotizacion para ese id y nombre.")
      self.__tipocotizaciones[tipo.id] = tipo
      return tipo

    def leer_por_id(self, id: int) -> Optional[TipoCotizacion]:
        """Retorna la categoría con el ID indicado, o None si no existe."""
        return self.__tipocotizaciones.get(id, None)

    def leer_todos(self) -> List[TipoCotizacion]:
        return list(self.__tipocotizaciones.values())

    def actualizar(self, entidad: TipoCotizacion) -> TipoCotizacion:
      """Actualiza un tipo de cotización existente. Lanza error si no existe."""
      if entidad.id not in self.__tipocotizaciones:
          raise ValueError("Moneda no encontrada.")
      self.__tipocotizaciones[entidad.id] = entidad
      return entidad

    def eliminar(self, id: int) -> bool:
      """Elimina el tipo de cotización con el ID indicado. Retorna True si se eliminó."""
      if id not in self.__tipocotizaciones:
          return False
      del self.__tipocotizaciones[id]
      return True


class RepositorioCotizacionDolar(IRepositorioCotizacionDolar):
  """Repositorio del tipo Cotizacion Dolar."""

  def __init__(self):
        """Inicializa el repositorio con un diccionario vacío."""
        self.__cotizaciones = {}  # { (tipo, fecha): CotizacionDolar }

  def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Crea una nueva cotización en el repositorio."""
        clave = (cotizacion.tipo.id, cotizacion.fecha)
        if clave in self.__cotizaciones:
            raise ValueError("Ya existe una cotización para ese tipo y fecha.")
        self.__cotizaciones[clave] = cotizacion
        return cotizacion

  def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: date) -> Optional[CotizacionDolar]:
        """Retorna la cotización para el tipo y fecha indicados, o None si no existe."""
        return self.__cotizaciones.get((tipo_id, fecha), None)

  def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
    """Retorna todas las cotizaciones históricas para el tipo indicado."""
    return [c for (t, f), c in self.__cotizaciones.items() if t == tipo_id]

  def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
    clave = (cotizacion.tipo.id, cotizacion.fecha)  # ← .id
    if clave not in self.__cotizaciones:
        raise ValueError("Cotización no encontrada.")
    self.__cotizaciones[clave] = cotizacion
    return cotizacion

  def eliminar(self, tipo_id: int, fecha: date) -> bool:
    clave = (tipo_id, fecha)
    if clave not in self.__cotizaciones:
        return False
    del self.__cotizaciones[clave]
    return True

