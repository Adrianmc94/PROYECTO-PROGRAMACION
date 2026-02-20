# model/usuarios.py

class Usuario:
    def __init__(self, id_user, username, password, rol="usuario"):
        self.id_user = id_user
        self.username = username
        self.__password = password  # Encapsulación (privado)
        self.rol = rol

    def verificar_password(self, pwd):
        return self.__password == pwd


    def __str__(self):
        return f"Usuario: {self.username} | Rol: {self.rol.upper()}"

class Admin(Usuario):
    def __init__(self, id_user, username, password):
        # Llamada al constructor del padre
        super().__init__(id_user, username, password, rol="admin")

    def tiene_permisos_totales(self):
        return True