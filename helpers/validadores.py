# helpers/validadores.py

def leer_entero(mensaje):
    """Valida que la entrada sea un número entero positivo."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("Error: El número no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Error: Por favor, introduce un número entero válido.")


def leer_float(mensaje):
    """Valida que la entrada sea un número decimal positivo."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("Error: El precio no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("Error: Por favor, introduce un número decimal válido.")

def confirmar_accion(mensaje):
    """Solicita confirmación al usuario (s/n)."""
    while True:
        res = input(f"{mensaje} (s/n): ").lower()
        if res in ['s', 'n']:
            return res == 's'
        print("Error: Responde con 's' para Sí o 'n' para No.")