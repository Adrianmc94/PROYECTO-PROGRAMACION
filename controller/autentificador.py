# controller/autenticador.py
from model.usuarios import Usuario, Admin

class Autenticador:
    def __init__(self, db_manager):
        self.db = db_manager

    def login(self, username, password):
        query = "SELECT * FROM usuarios WHERE username = ?"
        resultado = self.db.consultar(query, (username,))

        if resultado:
            user_data = resultado[0]
            # Creamos el objeto según el rol (POO: Herencia)
            if user_data['password'] == password:
                if user_data['rol'] == 'admin':
                    return Admin(user_data['id_usuario'], user_data['username'], user_data['password'])
                else:
                    return Usuario(user_data['id_usuario'], user_data['username'], user_data['password'])

    def registrar_usuario(self, username, password, rol):
        """Permite crear nuevos usuarios en la BBDD."""
        try:
            query = "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)"
            self.db.ejecutar_accion(query, (username, password, rol))
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

        return None