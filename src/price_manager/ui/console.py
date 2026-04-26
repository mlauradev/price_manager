
import os
from datetime import datetime, date
from price_manager.entities.entities import (
    Categoria, Proveedor, Producto, Precio, Moneda, CotizacionDolar, TipoCotizacion, Stock
)


class ConsoleUI:
    def __init__(self, srv_cat, srv_prov, srv_prod, srv_stock, srv_cot, srv_mon, srv_tipo_cot):
        self.srv_cat = srv_cat
        self.srv_prov = srv_prov
        self.srv_prod = srv_prod
        self.srv_stock = srv_stock
        self.srv_cot = srv_cot
        self.srv_mon = srv_mon
        self.srv_tipo_cot = srv_tipo_cot

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pausar(self):
        input("\nPresione Enter para continuar...")

    # MENÚ PRINCIPAL
    def menu_principal(self):
        while True:
            self.limpiar_pantalla()
            print("=" * 52)
            print("   SISTEMA DE GESTIÓN DE INVENTARIO - ELECTRÓNICA")
            print("=" * 52)
            print("  1. Gestionar Productos")
            print("  2. Gestionar Stock")
            print("  3. Gestionar Cotizaciones del Dólar")
            print("  4. Gestionar Categorías")
            print("  5. Gestionar Proveedores")
            print("  6. Gestionar Monedas")
            print("  7. Gestionar Tipos de Cotización")
            print("  0. Salir")
            print("=" * 52)

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.submenu_productos()
            elif opcion == "2":
                self.submenu_stock()
            elif opcion == "3":
                self.submenu_cotizaciones()
            elif opcion == "4":
                self.submenu_categorias()
            elif opcion == "5":
                self.submenu_proveedores()
            elif opcion == "6":
                self.submenu_monedas()
            elif opcion == "7":
                self.submenu_tipos_cotizacion()
            elif opcion == "0":
                print("\nSaliendo del sistema. ¡Hasta luego!")
                break
            else:
                print("Opción inválida.")
                self.pausar()

    # CRUD PRODUCTOS
    def submenu_productos(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE PRODUCTOS ---")
            print("1. Listar todos")
            print("2. Buscar por ID")
            print("3. Crear nuevo")
            print("4. Actualizar")
            print("5. Eliminar")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                self._listar_productos()
            elif opcion == "2":
                self._buscar_producto()
            elif opcion == "3":
                self._crear_producto()
            elif opcion == "4":
                self._actualizar_producto()
            elif opcion == "5":
                self._eliminar_producto()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
                self.pausar()

    def _listar_productos(self):
        self.limpiar_pantalla()
        print("-- LISTADO DE PRODUCTOS --\n")
        productos = self.srv_prod.listar_todos()
        if not productos:
            print("No hay productos registrados.")
        else:
            print(f"{'ID':<5} {'Nombre':<25} {'Precio':<12} {'Moneda':<8} {'Categoría':<15} {'Proveedor'}")
            print("-" * 80)
            for p in productos:
                print(f"{p.id:<5} {p.nombre:<25} {p.precio.valor:<12.2f} "
                      f"{p.precio.moneda.nombre:<8} {p.categoria.nombre:<15} {p.proveedor.nombre}")
        self.pausar()

    def _buscar_producto(self):
        self.limpiar_pantalla()
        try:
            id_p = int(input("ID del producto: "))
            p = self.srv_prod.obtener(id_p)
            print(f"\nID:          {p.id}")
            print(f"Nombre:      {p.nombre}")
            print(f"Descripción: {p.descripcion}")
            print(f"Precio:      {p.precio.valor:.2f} {p.precio.moneda.nombre}")
            print(f"Categoría:   {p.categoria.nombre}")
            print(f"Proveedor:   {p.proveedor.nombre}")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _crear_producto(self):
        self.limpiar_pantalla()
        print("-- ALTA DE PRODUCTO --\n")
        try:
            id_p = int(input("ID: "))
            nom = input("Nombre: ")
            desc = input("Descripción: ")
            val = float(input("Precio (valor): "))
            id_mon = int(input("ID Moneda: "))
            id_cat = int(input("ID Categoría: "))
            id_prov = int(input("ID Proveedor: "))

            moneda = self.srv_mon.obtener(id_mon)
            precio = Precio(valor=val, moneda=moneda)
            categoria = self.srv_cat.obtener(id_cat)
            proveedor = self.srv_prov.obtener(id_prov)

            nuevo_p = Producto(id=id_p, nombre=nom, descripcion=desc,
                               precio=precio, categoria=categoria, proveedor=proveedor)
            self.srv_prod.crear(nuevo_p)
            print("Producto creado con éxito.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _actualizar_producto(self):
        self.limpiar_pantalla()
        print("-- ACTUALIZAR PRODUCTO --\n")
        try:
            id_p = int(input("ID del producto a actualizar: "))
            p = self.srv_prod.obtener(id_p)
            print(f"Nombre actual: {p.nombre}  (Enter para mantener)")
            nom = input("Nuevo nombre: ").strip() or p.nombre
            desc = input(f"Nueva descripción ({p.descripcion}): ").strip() or p.descripcion
            val_str = input(f"Nuevo precio ({p.precio.valor}): ").strip()
            val = float(val_str) if val_str else p.precio.valor

            p.nombre = nom
            p.descripcion = desc
            p.precio.valor = val
            self.srv_prod.actualizar(p)
            print("Producto actualizado.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _eliminar_producto(self):
        self.limpiar_pantalla()
        print("-- ELIMINAR PRODUCTO --\n")
        try:
            id_p = int(input("ID del producto a eliminar: "))
            p = self.srv_prod.obtener(id_p)
            confirmar = input(f"¿Eliminar '{p.nombre}'? (s/n): ").strip().lower()
            if confirmar == 's':
                self.srv_prod.eliminar(id_p)
                print("Producto eliminado.")
            else:
                print("Operación cancelada.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    # CRUD STOCK
    def submenu_stock(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE STOCK ---")
            print("1. Ver stock de un producto")
            print("2. Crear stock inicial")
            print("3. Registrar movimiento (entrada/salida)")
            print("4. Eliminar stock")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                self._ver_stock()
            elif opcion == "2":
                self._crear_stock()
            elif opcion == "3":
                self._mover_stock()
            elif opcion == "4":
                self._eliminar_stock()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
                self.pausar()

    def _ver_stock(self):
        self.limpiar_pantalla()
        try:
            id_p = int(input("ID del producto: "))
            cantidad = self.srv_stock.obtener_stock(id_p)
            prod = self.srv_prod.obtener(id_p)
            print(f"\nProducto: {prod.nombre}")
            print(f"Stock disponible: {cantidad} unidades")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _crear_stock(self):
        self.limpiar_pantalla()
        print("-- CREAR STOCK INICIAL --\n")
        try:
            id_p = int(input("ID del producto: "))
            prod = self.srv_prod.obtener(id_p)
            almacen = input("Nombre del almacén: ")
            cantidad = int(input("Cantidad inicial: "))
            self.srv_stock.crear(prod, almacen, cantidad)
            print("Stock creado.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _mover_stock(self):
        self.limpiar_pantalla()
        print("-- MOVIMIENTO DE STOCK --\n")
        try:
            id_p = int(input("ID del producto: "))
            actual = self.srv_stock.obtener_stock(id_p)
            prod = self.srv_prod.obtener(id_p)
            print(f"Producto: {prod.nombre} | Stock actual: {actual}")
            mov = int(input("Cantidad (+ entrada / - salida): "))
            self.srv_stock.registrar_movimiento(id_p, mov)
            print("Movimiento registrado.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _eliminar_stock(self):
        self.limpiar_pantalla()
        print("-- ELIMINAR STOCK --\n")
        try:
            id_p = int(input("ID del producto: "))
            confirmar = input("¿Eliminar el registro de stock? (s/n): ").strip().lower()
            if confirmar == 's':
                self.srv_stock.eliminar_stock(id_p)
                print("Stock eliminado.")
            else:
                print("Operación cancelada.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    # CRUD COTIZACIONES
    def submenu_cotizaciones(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE COTIZACIONES ---")
            print("1. Ver historial por tipo")
            print("2. Registrar nueva cotización")
            print("3. Actualizar cotización")
            print("4. Eliminar cotización")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                self._ver_historico_cotizaciones()
            elif opcion == "2":
                self._crear_cotizacion()
            elif opcion == "3":
                self._actualizar_cotizacion()
            elif opcion == "4":
                self._eliminar_cotizacion()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")
                self.pausar()

    def _ver_historico_cotizaciones(self):
        self.limpiar_pantalla()
        try:
            id_tipo = int(input("ID tipo de cotización: "))
            historico = self.srv_cot.obtener_historico(id_tipo)
            if not historico:
                print("Sin datos históricos.")
            else:
                print(f"\n{'Fecha':<15} {'Valor':>10}")
                print("-" * 28)
                for c in historico:
                    print(f"{str(c.fecha):<15} ${c.valor:>9.2f}")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _crear_cotizacion(self):
        self.limpiar_pantalla()
        print("-- REGISTRAR COTIZACIÓN --\n")
        try:
            id_tipo = int(input("ID tipo de cotización: "))
            tipo = self.srv_tipo_cot.obtener(id_tipo)
            fecha_str = input("Fecha (YYYY-MM-DD): ")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            valor = float(input("Valor: "))
            cot = CotizacionDolar(valor=valor, fecha=fecha, tipo=tipo)
            self.srv_cot.registrar_cotizacion(cot)
            print("Cotización registrada.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _actualizar_cotizacion(self):
        self.limpiar_pantalla()
        print("-- ACTUALIZAR COTIZACIÓN --\n")
        try:
            id_tipo = int(input("ID tipo de cotización: "))
            tipo = self.srv_tipo_cot.obtener(id_tipo)
            fecha_str = input("Fecha de la cotización a modificar (YYYY-MM-DD): ")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            nuevo_valor = float(input("Nuevo valor: "))
            self.srv_cot.actualizar_cotizacion(nuevo_valor, fecha, tipo)
            print("Cotización actualizada.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    def _eliminar_cotizacion(self):
        self.limpiar_pantalla()
        print("-- ELIMINAR COTIZACIÓN --\n")
        try:
            id_tipo = int(input("ID tipo de cotización: "))
            tipo = self.srv_tipo_cot.obtener(id_tipo)
            fecha_str = input("Fecha (YYYY-MM-DD): ")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            confirmar = input("¿Confirmar eliminación? (s/n): ").strip().lower()
            if confirmar == 's':
                self.srv_cot.eliminar_cotizacion(tipo, fecha)
                print("Cotización eliminada.")
            else:
                print("Operación cancelada.")
        except ValueError as e:
            print(f"Error: {e}")
        self.pausar()

    # CRUD CATEGORÍAS
    def submenu_categorias(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE CATEGORÍAS ---")
            print("1. Listar todas")
            print("2. Crear nueva")
            print("3. Actualizar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                cats = self.srv_cat.listar_todos()
                print()
                for c in cats:
                    print(f"  ID: {c.id} | {c.nombre}")
                self.pausar()
            elif opcion == "2":
                try:
                    id_c = int(input("ID: "))
                    nom = input("Nombre: ")
                    self.srv_cat.crear(Categoria(id=id_c, nombre=nom))
                    print("Categoría creada.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "3":
                try:
                    id_c = int(input("ID a actualizar: "))
                    cat = self.srv_cat.obtener(id_c)
                    nom = input(f"Nuevo nombre ({cat.nombre}): ").strip() or cat.nombre
                    cat.nombre = nom
                    self.srv_cat.actualizar(cat)
                    print("Categoría actualizada.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "4":
                try:
                    id_c = int(input("ID a eliminar: "))
                    cat = self.srv_cat.obtener(id_c)
                    confirmar = input(f"¿Eliminar '{cat.nombre}'? (s/n): ").strip().lower()
                    if confirmar == 's':
                        self.srv_cat.eliminar(id_c)
                        print("Categoría eliminada.")
                    else:
                        print("Cancelado.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "0":
                break

    # CRUD PROVEEDORES
    def submenu_proveedores(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE PROVEEDORES ---")
            print("1. Listar todos")
            print("2. Crear nuevo")
            print("3. Actualizar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                provs = self.srv_prov.listar_todos()
                print()
                for p in provs:
                    print(f"  ID: {p.id} | {p.nombre} | {p.contacto}")
                self.pausar()
            elif opcion == "2":
                try:
                    id_p = int(input("ID: "))
                    nom = input("Nombre: ")
                    contacto = input("Contacto (mail/tel): ")
                    self.srv_prov.crear(Proveedor(id=id_p, nombre=nom, contacto=contacto))
                    print("Proveedor creado.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "3":
                try:
                    id_p = int(input("ID a actualizar: "))
                    prov = self.srv_prov.obtener(id_p)
                    nom = input(f"Nuevo nombre ({prov.nombre}): ").strip() or prov.nombre
                    contacto = input(f"Nuevo contacto ({prov.contacto}): ").strip() or prov.contacto
                    prov.nombre = nom
                    prov.contacto = contacto
                    self.srv_prov.actualizar(prov)
                    print("Proveedor actualizado.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "4":
                try:
                    id_p = int(input("ID a eliminar: "))
                    prov = self.srv_prov.obtener(id_p)
                    confirmar = input(f"¿Eliminar '{prov.nombre}'? (s/n): ").strip().lower()
                    if confirmar == 's':
                        self.srv_prov.eliminar(id_p)
                        print("Proveedor eliminado.")
                    else:
                        print("Cancelado.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "0":
                break

    # CRUD MONEDAS
    def submenu_monedas(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE MONEDAS ---")
            print("1. Listar todas")
            print("2. Crear nueva")
            print("3. Actualizar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                monedas = self.srv_mon.listar_todos()
                print()
                for m in monedas:
                    print(f"  ID: {m.id} | {m.nombre}")
                self.pausar()
            elif opcion == "2":
                try:
                    id_m = int(input("ID: "))
                    nom = input("Nombre (ej: ARS, USD): ")
                    self.srv_mon.crear(Moneda(id=id_m, nombre=nom))
                    print("Moneda creada.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "3":
                try:
                    id_m = int(input("ID a actualizar: "))
                    mon = self.srv_mon.obtener(id_m)
                    nom = input(f"Nuevo nombre ({mon.nombre}): ").strip() or mon.nombre
                    mon.nombre = nom
                    self.srv_mon.actualizar(mon)
                    print("Moneda actualizada.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "4":
                try:
                    id_m = int(input("ID a eliminar: "))
                    mon = self.srv_mon.obtener(id_m)
                    confirmar = input(f"¿Eliminar '{mon.nombre}'? (s/n): ").strip().lower()
                    if confirmar == 's':
                        self.srv_mon.eliminar(id_m)
                        print("Moneda eliminada.")
                    else:
                        print("Cancelado.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "0":
                break

    
    # CRUD TIPOS DE COTIZACIÓN
    def submenu_tipos_cotizacion(self):
        while True:
            self.limpiar_pantalla()
            print("--- GESTIÓN DE TIPOS DE COTIZACIÓN ---")
            print("1. Listar todos")
            print("2. Crear nuevo")
            print("0. Volver")

            opcion = input("\nSelección: ").strip()

            if opcion == "1":
                tipos = self.srv_tipo_cot.__repositorio.leer_todos() if hasattr(self.srv_tipo_cot, '_ServicioTipoCotizacion__repositorio') else []
                print()
                try:
                    from price_manager.repositories.repositories import RepositorioTipoCotizacion
                    tipos = self.srv_tipo_cot._ServicioTipoCotizacion__repositorio.leer_todos()
                    for t in tipos:
                        print(f"  ID: {t.id} | {t.nombre}")
                except Exception:
                    print("  (Listado no disponible directamente)")
                self.pausar()
            elif opcion == "2":
                try:
                    id_t = int(input("ID: "))
                    nom = input("Nombre (ej: Blue, Oficial): ")
                    self.srv_tipo_cot.crear(TipoCotizacion(id=id_t, nombre=nom))
                    print("Tipo de cotización creado.")
                except ValueError as e:
                    print(f"Error: {e}")
                self.pausar()
            elif opcion == "0":
                break


def start_ui(srv_cat, srv_prov, srv_prod, srv_stock, srv_cot, srv_mon, srv_tipo_cot):
    ui = ConsoleUI(srv_cat, srv_prov, srv_prod, srv_stock, srv_cot, srv_mon, srv_tipo_cot)
    ui.menu_principal()
