# controller/gestion_almacen.py
from model.articulos import Juego
from helpers.excepciones import SinStockError, DatabaseError
from helpers.generador_archivos import guardar_ticket_txt, exportar_inventario_json

class GestionAlmacen:
    def __init__(self, db_manager):
        self.db = db_manager
        # REQUISITO: Diccionario para localización rápida por ID
        self.inventario_memoria = {}
        # REQUISITO: Lista de preparación para envíos
        self.lista_preparacion = []
        self.cargar_inventario_desde_db()

    def cargar_inventario_desde_db(self):
        """Carga los datos de la BBDD al diccionario en memoria."""
        try:
            filas = self.db.consultar("SELECT * FROM productos")
            self.inventario_memoria = {
                f['id_producto']: Juego(
                    f['id_producto'], f['nombre'], f['precio'],
                    f['stock'], f['plataforma'], f['genero']
                ) for f in filas
            }
        except DatabaseError as e:
            print(f"Error al sincronizar con BBDD: {e}")

    def mostrar_inventario(self):
        if not self.inventario_memoria:
            print("\nEl almacén está vacío.")
        else:
            print("\n--- INVENTARIO ACTUAL ---")
            for juego in self.inventario_memoria.values():
                print(juego)

    def preparar_salida(self, id_prod, cantidad):
        if id_prod not in self.inventario_memoria:
            print("Error: El producto no existe.")
            return

        juego = self.inventario_memoria[id_prod]

        if juego.stock < cantidad:
            raise SinStockError(juego.nombre, cantidad, juego.stock)

        self.lista_preparacion.append({
            'id': id_prod,
            'nombre': juego.nombre,
            'cantidad': cantidad
        })
        print(f"Añadido: {juego.nombre} (x{cantidad}) a la lista de preparación.")

    def confirmar_pedido(self, usuario):
        if not self.lista_preparacion:
            print("La lista de preparación está vacía.")
            return

        try:
            for item in self.lista_preparacion:
                # 1. Actualizar objeto en memoria
                juego = self.inventario_memoria[item['id']]
                juego.stock -= item['cantidad']

                # 2. Actualizar BBDD
                self.db.ejecutar_accion(
                    "UPDATE productos SET stock = ? WHERE id_producto = ?",
                    (juego.stock, item['id'])
                )

                # 3. Registrar movimiento
                self.db.ejecutar_accion(
                    "INSERT INTO movimientos (id_producto, id_usuario, cantidad, tipo) VALUES (?, ?, ?, ?)",
                    (item['id'], usuario.id_user, item['cantidad'], 'SALIDA')
                )

            guardar_ticket_txt(self.lista_preparacion, usuario.username)
            print("\nPedido confirmado. Ticket generado.")
            self.lista_preparacion = []

        except Exception as e:
            print(f"Error crítico al procesar pedido: {e}")

    def realizar_backup(self):
        """ESTA FUNCIÓN DEBE ESTAR DENTRO DE LA CLASE (Indentada con 4 espacios)"""
        if not self.inventario_memoria:
            print("No hay datos en el inventario para exportar.")
            return

        # Convertimos los objetos a diccionarios usando to_dict()
        datos_json = [j.to_dict() for j in self.inventario_memoria.values()]

        mensaje = exportar_inventario_json(datos_json)
        print(mensaje)