# helpers/excepciones.py

class AlmacenError(Exception):
    """Clase base para excepciones del sistema"""
    pass

class SinStockError(AlmacenError):
    """Lanzada cuando se intenta retirar más de lo que hay"""
    def __init__(self, producto, solicitado, disponible):
        self.mensaje = f"Error: '{producto}' solo tiene {disponible} unidades (Pediste {solicitado})."
        super().__init__(self.mensaje)


class DatabaseError(AlmacenError):
    """Lanzada cuando falla la conexión o una consulta SQL"""
    pass

