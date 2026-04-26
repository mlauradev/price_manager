import csv
import os
from datetime import datetime
from price_manager.entities.entities import (
    Categoria, Proveedor, Moneda, Precio, Producto, Stock, CotizacionDolar, TipoCotizacion
)

def preload_data(srv_cat, srv_prov, srv_mon, srv_prod, srv_stock, srv_tipo_cot, srv_cot):
    """
    Lee los archivos CSV de la carpeta migrations/csv y carga los datos
    usando los servicios inyectados.
    """

    # Ruta base a los archivos CSV
    base_path = "price_manager/migrations/csv/"

    # 1. Cargar Categorías
    with open(os.path.join(base_path, 'categorias.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = Categoria(id=int(row['id']), nombre=row['nombre'])
            srv_cat.crear(cat)

    # 2. Cargar Proveedores
    with open(os.path.join(base_path, 'proveedores.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prov = Proveedor(id=int(row['id']), nombre=row['nombre'], contacto=row['contacto'])
            srv_prov.crear(prov)

    # 3. Cargar Monedas
    with open(os.path.join(base_path, 'monedas.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mon = Moneda(id=int(row['id']), nombre=row['nombre'])
            srv_mon.crear(mon)

    # 4. Cargar Tipos de Cotización
    with open(os.path.join(base_path, 'tipos_cotizaciones.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tipo = TipoCotizacion(id=int(row['id']), nombre=row['nombre'])
            srv_tipo_cot.crear(tipo)

    # 5. Cargar Productos
    with open(os.path.join(base_path, 'productos.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # IMPORTANTE: Usar las columnas de relación, no el 'id' del producto
            moneda = srv_mon.obtener(int(row['id_moneda']))
            precio = Precio(valor=float(row['valor']), moneda=moneda)
            cat = srv_cat.obtener(int(row['id_categoria']))
            prov = srv_prov.obtener(int(row['id_proveedor']))

            prod = Producto(
                id=int(row['id']),
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                precio=precio,
                categoria=cat,
                proveedor=prov
            )
            srv_prod.crear(prod)

    # 6. Cargar Stock
    with open(os.path.join(base_path, 'stock.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Usar 'id_producto' que es la columna del CSV
            producto = srv_prod.obtener(int(row['id_producto']))
            srv_stock.crear(producto, row['almacen'], int(row['cantidad']))

    # 7. Cargar Cotizaciones
    with open(os.path.join(base_path, 'cotizaciones_dolar.csv'), mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Usar 'id_tipo' para buscar el tipo de dólar
            tipo = srv_tipo_cot.obtener(int(row['id_tipo']))
            fecha = datetime.strptime(row['fecha'], "%Y-%m-%d").date()
            cot = CotizacionDolar(valor=float(row['valor']), fecha=fecha, tipo=tipo)
            srv_cot.registrar_cotizacion(cot)

    print("¡Datos precargados exitosamente desde CSV!")
