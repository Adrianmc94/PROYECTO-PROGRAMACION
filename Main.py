import sys
import os

from database.conexion import DBConexion
from database.consultas import inicializar_bbdd
from controller.autentificador import  Autenticador
from controller.gestion_almacen import GestionAlmacen
from helpers.validadores import leer_entero, leer_float, confirmar_accion
from helpers.excepciones import SinStockError, AlmacenError

def menu_principal(usuario, gestion, auth):
    while True:
        print(f"\nSESIÓN: {usuario.username.upper()} ({usuario.rol})")
        print("1. Consultar inventario")
        print("2. Registrar salida de producto")
        print("3. Confirmar pedido (Generar ticket)")

        if usuario.rol == "admin":
            print("4. Añadir un nuevo producto (ADMIN)")
            print("5. Exportar backup en JSON  (ADMIN)")
            print("6. Registrar nuevo usuario (ADMIN)")

        print("0. Cerrar sesión")

        opcion = input("\nSeleccione una opción: ")

        try:
            if opcion == "1":
                gestion.mostrar_inventario()

            elif opcion == "2":
                id_p = leer_entero("ID del producto: ")
                cant = leer_entero("Cantidad: ")
                gestion.preparar_salida(id_p, cant)

            elif opcion == "3":
                if confirmar_accion("¿Confirmar el pedido actual?"):
                    gestion.confirmar_pedido(usuario)

            elif opcion == "4" and usuario.rol == "admin":
                nom = input("Nombre: ")
                pre = leer_float("Precio: ")
                stk = leer_entero("Stock inicial: ")
                plat = input("Plataforma: ")
                gen = input("Género: ")

                gestion.db.ejecutar_accion(
                    "INSERT INTO productos (nombre, precio, stock, plataforma, genero) VALUES (?,?,?,?,?)",
                    (nom, pre, stk, plat, gen)
                )
                gestion.cargar_inventario_desde_db()
                print("Producto registrado.")

            elif opcion == "5" and usuario.rol == "admin":
                gestion.realizar_backup()

            elif opcion == "6" and usuario.rol == "admin":
                u = input("Nombre de usuario: ")
                p = input("Contraseña: ")
                r = input("Rol (admin/usuario): ").lower()
                if r in ['admin', 'usuario']:
                    if auth.registrar_usuario(u, p, r):
                        print(f"Usuario '{u}' creado.")
                else:
                    print("Error: Rol no válido.")

            elif opcion == "0":
                break
            else:
                print("Opción no válida.")

        except SinStockError as e:
            print(f"Error de stock: {e}")
        except AlmacenError as e:
            print(f"Error del sistema: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

def main():
    db = DBConexion()
    try:
        inicializar_bbdd(db)
    except Exception as e:
        print(f"Error al iniciar base de datos: {e}")
        return

    auth = Autenticador(db)
    gestion = GestionAlmacen(db)

    print("SISTEMA DE GESTIÓN DE INVENTARIO")

    intentos = 0
    while intentos < 3:
        user = input("\nUsuario: ")
        pw = input("Contraseña: ")

        usuario_logueado = auth.login(user, pw)

        if usuario_logueado:
            menu_principal(usuario_logueado, gestion, auth)
            break
        else:
            intentos += 1
            print(f"Credenciales incorrectas. Intentos restantes: {3 - intentos}")

if __name__ == "__main__":
    main()