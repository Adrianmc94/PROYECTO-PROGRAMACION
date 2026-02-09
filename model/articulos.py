# model/articulos.py

class Articulo:
    def __init__(self, id_prod, nombre, precio, stock):
        self.id_prod = id_prod
        self.nombre = nombre
        self._precio = precio  # Protegido
        self._stock = stock    # Protegido

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise ValueError("No hay suficiente stock disponible.")
        self._stock = valor

class Juego(Articulo):
    def __init__(self, id_prod, nombre, precio, stock, plataforma, genero):
        super().__init__(id_prod, nombre, precio, stock)
        self.plataforma = plataforma
        self.genero = genero

    def __str__(self):
        return f"ID: {self.id_prod} | [{self.plataforma}] {self.nombre} - {self.precio}€ (Stock: {self.stock})"

    def to_dict(self):
        """Método auxiliar para facilitar el Backup JSON"""
        return {
            "id": self.id_prod,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "plataforma": self.plataforma,
            "genero": self.genero
        }