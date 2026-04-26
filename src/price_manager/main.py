from datetime import date, datetime
import sys
from price_manager.repositories.repositories import (
    RepositorioCategoria, RepositorioProveedor, RepositorioMoneda,
    RepositorioTipoCotizacion, RepositorioProducto, RepositorioStock,
    RepositorioCotizacionDolar
)
from price_manager.services.services import (
    ServicioCategoria, ServicioProveedor, ServicioMoneda,
    ServicioTipoCotizacion, ServicioProducto, ServicioStock,
    ServicioCotizacionDolar
)
from price_manager.preload_data.preload_data import preload_data
from price_manager.ui.console import start_ui

def main(import_default_data: bool = False):
    print("--- Inicializando Sistema de Gestión de Inventarios ---")

    # 1. Instanciar Repositorios (Persistencia)
    repo_cat = RepositorioCategoria()
    repo_prov = RepositorioProveedor()
    repo_mon = RepositorioMoneda()
    repo_tipo_cot = RepositorioTipoCotizacion()
    repo_prod = RepositorioProducto()
    repo_stock = RepositorioStock()
    repo_cot = RepositorioCotizacionDolar()

    # 2. Instanciar Servicios (Lógica de Negocio e Inyección de Dependencias)
    srv_cat = ServicioCategoria(repo_cat)
    srv_prov = ServicioProveedor(repo_prov)
    srv_mon = ServicioMoneda(repo_mon)
    srv_tipo_cot = ServicioTipoCotizacion(repo_tipo_cot)

    # Producto necesita los servicios de Cat y Prov para validar
    srv_prod = ServicioProducto(repo_prod, srv_cat, srv_prov)

    # Stock necesita el servicio de Producto
    srv_stock = ServicioStock(repo_stock, srv_prod)

    # Cotización necesita el servicio de Tipo para validar históricos
    srv_cot = ServicioCotizacionDolar(repo_cot, srv_tipo_cot)

    # 3. Carga Opcional de Datos (Migrations)
    if import_default_data:
        try:
            preload_data(srv_cat, srv_prov, srv_mon, srv_prod, srv_stock, srv_tipo_cot, srv_cot)
        except Exception as e:
            print(f" Error al precargar datos: {e}")

    # 4. Lanzar Interfaz de Usuario
    try:
        start_ui(srv_cat, srv_prov, srv_prod, srv_stock, srv_cot, srv_mon, srv_tipo_cot)
    except KeyboardInterrupt:
        print("\nPrograma finalizado por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    # Si se ejecuta este archivo directamente, por defecto cargamos los CSV
    main(import_default_data=True)
