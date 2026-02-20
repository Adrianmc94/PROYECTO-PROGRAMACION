# helpers/generador_archivos.py
import json
import os
from datetime import datetime

def guardar_ticket_txt(pedido, usuario_nombre):
    """Genera un ticket de salida único con fecha y hora"""
    os.makedirs("data/tickets", exist_ok=True)
    # Nombre único para evitar que parezca que no se actualiza
    fecha_hoy = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/tickets/ticket_{usuario_nombre}_{fecha_hoy}.txt"


    with open(filename, "w", encoding="utf-8") as f:
        f.write("--- TICKET DE SALIDA DE ALMACÉN ---\n")
        f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Usuario: {usuario_nombre}\n")
        f.write("-" * 35 + "\n")
        for item in pedido:
            f.write(f"{item['nombre']} x{item['cantidad']}\n")
        f.write("-" * 35 + "\n")
        f.write("Operación realizada con éxito.")

def exportar_inventario_json(lista_productos):
    """Exporta todo el stock a un backup JSON"""
    os.makedirs("data/backups", exist_ok=True)
    ruta = "data/backups/inventario.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(lista_productos, f, indent=4, ensure_ascii=False)
    return f"Backup creado en {ruta}"