
from typing import List, Optional
from datetime import date

# Importamos las entidades
from price_manager.entities.entities import (
    EntidadBase, Categoria, Proveedor, Producto,
    Stock, CotizacionDolar, Precio, Moneda, TipoCotizacion
)

# IMPORTANTE: Importamos los repositorios para que el Type Hint funcione
from price_manager.repositories.repositories import (
    RepositorioCategoria, RepositorioProveedor, RepositorioProducto,
    RepositorioStock, RepositorioMoneda, RepositorioTipoCotizacion,
    RepositorioCotizacionDolar
)


# Defino clase ServicioCategoria
class ServicioCategoria:
    """Gestiona la lógica de negocio para las operaciones sobre Categoria."""

    def __init__(self, repositorio: RepositorioCategoria):
        """Inicializa el servicio con su repositorio correspondiente."""
        self.__repositorio = repositorio

    def crear(self, categoria:Categoria) -> Categoria:
        """
        Crea una nueva categoría verificando que el nombre no esté duplicado.

        Args:
            categoria (Categoria): Instancia de Categoría.

        Returns:
            Categoria: La categoría creada.
        """
        for cat in self.__repositorio.leer_todos():
            if cat.nombre.lower() == categoria.nombre.lower():
                raise ValueError(f"Ya existe una categoría con el nombre '{categoria.nombre}'.")
        return self.__repositorio.crear(categoria)

    def obtener(self, id: int) -> Categoria:
        """
        Retorna una categoría por su ID. Lanza error si no existe.

        Args:
            id (int): Identificador de la categoría a buscar.

        Returns:
            Categoria: La categoría encontrada.
        """
        categoria = self.__repositorio.leer_por_id(id)
        if not categoria:
            raise ValueError(f"No existe una categoría con el ID {id}.")
        return categoria

    def listar_todos(self) -> List[Categoria]:
        """
        Retorna todas las categorías almacenadas.

        Returns:
            List[Categoria]: Lista con todas las categorías.
        """
        return self.__repositorio.leer_todos()

    def actualizar(self, categoria: Categoria) -> Categoria:
        """
        Actualiza una categoría existente en el repositorio.

        Args:
            categoria (Categoria): El objeto categoría con los datos ya modificados.

        Returns:
            Categoria: La categoría actualizada.

        Raises:
            ValueError: Si la categoría no existe en el repositorio.
        """
        # Primero verificamos si existe llamando a nuestro propio método obtener
        # Si no existe, obtener() lanzará el ValueError que el test espera.
        self.obtener(categoria.id)

        # Si esta, entonces lo actualizamos
        return self.__repositorio.actualizar(categoria)

    def eliminar(self, id: int) -> bool:
        """
        Elimina una categoría por su ID.

        Args:
           id (int): Identificador de la categoría a eliminar.

        Returns:
            bool: True si se eliminó correctamente.
        """
        self.obtener(id)
        return self.__repositorio.eliminar(id)


# Defino clase ServicioProveedor

class ServicioProveedor:
    """Gestiona la lógica de negocio para las operaciones sobre Proveedor."""

    def __init__(self, repositorio: RepositorioProveedor):
        """Inicializa el servicio con su repositorio correspondiente."""
        self.__repositorio = repositorio

    def crear(self, proveedor:Proveedor) -> Proveedor:
        """
        Crea un nuevo proveedor verificando que el nombre no esté duplicado.

        Args:
            proveedor (Proveedor): Instancia de Proveedor

        Returns:
            Proveedor: El proveedor creado.
        """
        for prov in self.__repositorio.leer_todos():
            if prov.nombre.lower() == proveedor.nombre.lower():
                raise ValueError(f"Ya existe un proveedor con el nombre '{proveedor.nombre}'.")
        return self.__repositorio.crear(proveedor)

    def obtener(self, id_proveedor: int) -> Proveedor:
        """
        Retorna un proveedor por su ID. Lanza error si no existe.

        Args:
            id_proveedor (int): Identificador del proveedor a buscar.

        Returns:
            Proveedor: El proveedor encontrado.
        """
        proveedor = self.__repositorio.leer_por_id(id_proveedor)
        if not proveedor:
            raise ValueError(f"No existe un proveedor con el ID {id_proveedor}.")
        return proveedor

    def listar_todos(self) -> List[Proveedor]:
        """
        Retorna todos los proveedores almacenados.

        Returns:
            List[Proveedor]: Lista con todos los proveedores.
        """
        return self.__repositorio.leer_todos()

    def actualizar(self, proveedor: Proveedor) -> Proveedor:
        """
        Actualiza los datos de un proveedor existente.

        Args:
            proveedor (Proveedor): Instancia de Proveedor

        Returns:
            Proveedor: El proveedor actualizado.
        """
        self.obtener(proveedor.id) # Valida que exista
        return self.__repositorio.actualizar(proveedor)

    def eliminar(self, id_proveedor: int) -> bool:
        """
        Elimina un proveedor por su ID.

        Args:
            id_proveedor (int): Identificador del proveedor a eliminar.

        Returns:
            bool: True si se eliminó correctamente.
        """
        self.obtener(id_proveedor)
        return self.__repositorio.eliminar(id_proveedor)

# Defino clase ServicioProducto

class ServicioProducto:
    """Gestiona la lógica de negocio para las operaciones sobre Producto."""

    def __init__(self, repositorio: RepositorioProducto, servicio_cat: ServicioCategoria, servicio_prov: ServicioProveedor):
        self.__repositorio = repositorio
        self.__srv_cat = servicio_cat
        self.__srv_prov = servicio_prov

    def crear(self, producto: Producto) -> Producto:
        """
        Crea un nuevo producto verificando que el nombre no esté duplicado.

        Args:
            producto (Producto): Instancia de Producto
        Returns:
            Producto: El producto creado.
        """

        # Validar que categoría y proveedor existan realmente
        self.__srv_cat.obtener(producto.categoria.id)
        self.__srv_prov.obtener(producto.proveedor.id)

        for prod in self.__repositorio.leer_todos():
            if prod.nombre.lower() == producto.nombre.lower():
                raise ValueError(f"Ya existe un producto con el nombre '{producto.nombre}'.")
        return self.__repositorio.crear(producto)

    def listar_todos(self) -> List[Producto]:
        """
        Retorna todos los productos almacenados.
        """
        return self.__repositorio.leer_todos()

    def obtener(self, id_producto: int) -> Producto:
        """
        Retorna un producto por su ID. Lanza error si no existe.

        Args:
            id_producto (int): Identificador del producto a buscar.

        Returns:
            Producto: El producto encontrado.
        """
        producto = self.__repositorio.leer_por_id(id_producto)
        if not producto:
            raise ValueError(f"No existe un producto con el ID {id_producto}.")
        return producto

    def actualizar(self, producto: Producto) -> Producto:
        """
        Actualiza los datos de un producto existente.

        Args:
             producto (Producto): Instancia de Producto
        Returns:
            Producto: El producto actualizado.
        """
        self.obtener(producto.id)  # Valida existencia, lanza ValueError si no existe
        return self.__repositorio.actualizar(producto)

    def eliminar(self, id_producto: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            id_producto (int): Identificador del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente.
        """
        self.obtener(id_producto)
        return self.__repositorio.eliminar(id_producto)

    def precio_en_usd(self, id_producto: int, cotizacion: CotizacionDolar) -> float:
        """

        Convierte el precio de un producto a USD usando la cotización indicada.

        Args:
            id_producto (int): Identificador del producto.
            cotizacion (CotizacionDolar): Cotización a utilizar para la conversión.

        Returns:
            float: Precio del producto expresado en USD.
        """
        producto = self.obtener(id_producto)

        # Accedemos al nombre o atributo que identifica la moneda (ej: .nombre)
        moneda_codigo = producto.precio.moneda.nombre.upper()

        if moneda_codigo == "USD":
            return producto.precio.valor

        if moneda_codigo == "ARS":
            # Usamos el valor de la cotización que recibimos por parámetro
            return round(producto.precio.valor / cotizacion.valor, 2)

        raise ValueError(f"Conversión desde {moneda_codigo} no soportada.")

# Defino clase ServicioStock

class ServicioStock:
    """Gestiona la lógica de negocio para las operaciones sobre Stock."""

    def __init__(self, repositorio: RepositorioStock, srv_prod: ServicioProducto):
        """Inicializa el servicio con su repositorio correspondiente."""
        self.__repositorio = repositorio
        self.__srv_prod = srv_prod

    def crear(self, producto: Producto, almacen: str, cantidad: int) -> Stock:
        """
        Crea un nuevo registro de stock para un producto.

        Args:
            producto (Producto): Instancia del producto a almacenar.
            almacen (str): Nombre del almacén donde se encuentra el producto.
            cantidad (int): Cantidad inicial disponible.

        Returns:
            Stock: El registro de stock creado.
        """
        stock = Stock(producto, almacen, cantidad)
        return self.__repositorio.crear(stock)

    def obtener_stock(self, producto_id: int):
        """
        Retorna el stock de un producto por su ID. Lanza error si no existe.

        Args:
            producto_id (int): Identificador del producto.

        Returns:
            Stock: El registro de stock encontrado.
        """
        stock = self.__repositorio.leer_por_producto(producto_id)
        if not stock:
            raise ValueError("Stock no encontrado.")
        return stock.cantidad

    def registrar_movimiento(self, producto_id: int, unidades: int) -> Stock:
        """
        Registra movimientos al stock de un producto existente.

        Args:
            producto_id (int): Identificador del producto.
            unidades (int): Cantidad de unidades a agregar.

        Returns:
            Stock: El stock actualizado.
        """
        stock = self.__repositorio.leer_por_producto(producto_id)
        if not stock:
            # Si no existe, lo creamos automáticamente con cantidad 0
            producto = self.__srv_prod.obtener(producto_id)
            stock = Stock(producto, "Principal", 0)
            self.__repositorio.crear(stock)

        nuevo_total = stock.cantidad + unidades
        if nuevo_total < 0:
            raise ValueError("La operación resultaría en stock negativo.")

        stock.cantidad = nuevo_total
        return self.__repositorio.actualizar(stock)

    def eliminar_stock(self, producto_id: int) -> bool:
        """
        Elimina el registro de stock de un producto.

        Args:
            producto_id (int): Identificador del producto.

        Returns:
            bool: True si se eliminó correctamente.
        """
        self.obtener_stock(producto_id)
        return self.__repositorio.eliminar(producto_id)

# Defino clase ServicioTipoCotizacion
class ServicioTipoCotizacion:
  """Inicializa el servicio con su repositorio correspondiente."""

  def __init__(self, repositorio: RepositorioTipoCotizacion):
        self.__repositorio = repositorio

  def crear(self,tipo:TipoCotizacion) -> TipoCotizacion:
      """
      Crea un nuevo tipo de cotización verificando que el tipo no sea nulo.

      Args:
          tipo (TipoCotizacion): Tipo de cambio (ej: 'Oficial', 'Blue').

      Returns:
          TipoCotizacion: El tipo  creada.
      """
      return self.__repositorio.crear(tipo)

  def obtener(self, id: int) -> TipoCotizacion:
        tipo = self.__repositorio.leer_por_id(id)
        if not tipo:
            raise ValueError(f"No existe el tipo con ID {id}")
        return tipo

# Defino clase ServicioCotizacionDolar
class ServicioCotizacionDolar:
    """Gestiona la lógica de negocio para las operaciones sobre CotizacionDolar."""

    def __init__(self, repositorio: RepositorioCotizacionDolar, srv_tipo: ServicioTipoCotizacion):
        """Inicializa el servicio con su repositorio correspondiente."""
        self.__repositorio = repositorio
        self.__srv_tipo = srv_tipo

    def crear(self, valor: float, fecha: date, tipo: TipoCotizacion) -> CotizacionDolar:
        """
        Crea una nueva cotización verificando que el valor sea positivo.

        Args:
            valor (float): Valor de la cotización. Debe ser mayor a cero.
            fecha (date): Fecha de la cotización.
            tipo (str): Tipo de cambio (ej: 'Oficial', 'Blue').

        Returns:
            CotizacionDolar: La cotización creada.
        """
        if valor <= 0:
            raise ValueError("El valor de la cotización debe ser mayor a cero.")
        cotizacion = CotizacionDolar(valor, fecha, tipo)
        return self.__repositorio.crear(cotizacion)

    def obtener_cotizacion(self, tipo: TipoCotizacion, fecha: date) -> CotizacionDolar:
        """
        Retorna una cotización por tipo y fecha. Lanza error si no existe.

        Args:
            tipo (str): Tipo de cambio a buscar.
            fecha (date): Fecha de la cotización a buscar.

        Returns:
            CotizacionDolar: La cotización encontrada.
        """
        cotizacion = self.__repositorio.leer_por_tipo_y_fecha(tipo, fecha)
        if cotizacion is None:
            raise ValueError(f"No existe cotización de tipo '{tipo}' para la fecha {fecha}.")
        return cotizacion

    def obtener_historico(self, tipo_id: int):
        """
        Retorna el historial de cotizaciones para un tipo id dado.

        Args:
            tipo (str): Tipo de cambio del cual obtener el historial.
        Returns:
            List[CotizacionDolar]: Lista de cotizaciones históricas.
        """
        self.__srv_tipo.obtener(tipo_id)
        return self.__repositorio.leer_historico_por_tipo(tipo_id)

    def actualizar_cotizacion(self, valor: float, fecha: date, tipo: TipoCotizacion) -> CotizacionDolar:
        """
        Actualiza el valor de una cotización existente.

        Args:
            valor (float): Nuevo valor de la cotización.
            fecha (date): Fecha de la cotización a actualizar.
            tipo (str): Tipo de cambio a actualizar.

        Returns:
            CotizacionDolar: La cotización actualizada.
        """
        cotizacion = self.obtener_cotizacion(tipo, fecha)
        cotizacion.valor = valor
        return self.__repositorio.actualizar(cotizacion)

    def eliminar_cotizacion(self, tipo: TipoCotizacion, fecha: date) -> bool:
        """
        Elimina una cotización por tipo y fecha.

        Args:
            tipo (str): Tipo de cambio a eliminar.
            fecha (date): Fecha de la cotización a eliminar.

        Returns:
            bool: True si se eliminó correctamente.
        """
        self.obtener_cotizacion(tipo, fecha)
        return self.__repositorio.eliminar(tipo, fecha)

    def registrar_cotizacion(self, cotizacion:CotizacionDolar):
        """
        Registra una cotización en el repositorio.

        Args:
            cotizacion: CotizaciónDolar a registrar

        """
        self.__srv_tipo.obtener(cotizacion.tipo.id) 
        self.__repositorio.crear(cotizacion)


# Defino clase ServicioMoneda
class ServicioMoneda:
  """Inicializa el servicio con su repositorio correspondiente."""

  def __init__(self, repositorio: RepositorioMoneda):
        self.__repositorio = repositorio

  def crear(self, moneda: Moneda) -> Moneda:
      """
      Crea un nuevo tipo de Moneda verificando que el tipo no sea nulo.

      Args:
          tipo_moneda (Moneda): Tipo de Moneda (ej: 'ARS', 'USD').

      Returns:
          Moneda: Moneda  creada.
      """
      for mon in self.__repositorio.leer_todos():
          if mon.nombre.lower() == moneda.nombre.lower():
              raise ValueError(f"Ya existe una categoría con el nombre '{moneda.nombre}'.")
      return self.__repositorio.crear(moneda)


  def obtener(self, id_moneda: int) -> Moneda:
      moneda = self.__repositorio.leer_por_id(id_moneda)
      if not moneda:
          raise ValueError(f"No existe la categoría con ID {id_moneda}")
      return moneda

  def listar_todos(self):
      return self.__repositorio.leer_todos()

  def actualizar(self, moneda: Moneda) -> Moneda:
      self.obtener(moneda.id) # Valida que exista
      return self.__repositorio.actualizar(moneda)

  def eliminar(self, id_moneda: int):
      self.obtener(id_moneda) # Valida que exista
      return self.__repositorio.eliminar(id_moneda)
