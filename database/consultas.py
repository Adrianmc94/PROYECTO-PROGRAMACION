# database/consultas.py

def inicializar_bbdd(db):
    # Definimos las tablas
    tablas = [
        """CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            plataforma TEXT,
            genero TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS movimientos (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER,
            id_usuario INTEGER,
            cantidad INTEGER,
            tipo TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(id_producto) REFERENCES productos(id_producto),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        )"""
    ]

    for tabla in tablas:
        db.ejecutar_accion(tabla)

    # Creamos un admin por defecto si la tabla está vacía
    usuarios = db.consultar("SELECT * FROM usuarios")
    if not usuarios:
        db.ejecutar_accion(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            ("admin", "1234", "admin")
        )
        print("BBDD Inicializada. Usuario por defecto: admin / 1234")