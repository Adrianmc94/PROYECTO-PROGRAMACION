# database/conexion.py
import sqlite3
import os
from helpers.excepciones import DatabaseError

class DBConexion:
    def __init__(self, ruta_db="data/almacen.db"):
        # Aseguramos que la carpeta data exista
        os.makedirs(os.path.dirname(ruta_db), exist_ok=True)
        self.ruta = ruta_db

    def conectar(self):
        try:
            conn = sqlite3.connect(self.ruta)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Error de conexión: {e}")

    def ejecutar_accion(self, query, params=()):
        """Para INSERT, UPDATE, DELETE"""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise DatabaseError(f"Error en SQL: {e}")

    def consultar(self, query, params=()):
        """Para SELECT (devuelve todos los resultados)"""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise DatabaseError(f"Error en consulta: {e}")