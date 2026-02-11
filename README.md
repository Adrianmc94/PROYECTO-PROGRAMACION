# Gestión de Inventario

Este proyecto consiste en una aplicación de gestión de inventario desarrollada en **Python**, diseñada para centralizar el control de **stock**, **usuarios** y **movimientos de almacén**.  
La aplicación implementa persistencia de datos mediante una base de datos relacional **SQLite** y generación de archivos externos en formatos **JSON** y **TXT**.

## Estructura del Proyecto

El código se organiza siguiendo una estructura modular para separar la lógica de negocio, los modelos de datos y la persistencia:

- **Main.py**: Punto de entrada de la aplicación y gestión del menú principal.
- **model/**: Contiene las definiciones de clases como `Articulo`, `Juego`, `Usuario` y `Admin`.
- **controller/**: Módulos de lógica como `GestionAlmacen` y `Autenticador`.
- **database/**: Gestión de la conexión a la base de datos y ejecución de scripts SQL.
- **helpers/**: Herramientas auxiliares para validación de entrada, excepciones personalizadas y generación de archivos.

## Características Técnicas

### 1. Programación Orientada a Objetos (POO)

El sistema utiliza herencia para especializar el comportamiento de los objetos:

- **Usuarios**: La clase `Admin` hereda de `Usuario`, permitiendo el acceso a funciones restringidas como backups y registro de nuevos perfiles.
- **Productos**: La clase `Juego` hereda de `Articulo`, añadiendo atributos específicos como plataforma y género.

Se aplica **encapsulación** mediante decoradores `@property` para proteger atributos sensibles como el precio y el stock, asegurando que no se asignen valores negativos.
```python
@property
def stock(self):
    return self._stock

@stock.setter
def stock(self, valor):
    if valor < 0:
        raise ValueError("No hay suficiente stock disponible.")
    self._stock = valor
```

### 2. Gestión de Persistencia y Archivos

La aplicación utiliza tres métodos de persistencia:

- **SQLite**: Almacena de forma permanente juegos, usuarios y el historial de movimientos.
- **JSON**: Permite realizar copias de seguridad completas del inventario actual mediante el método `to_dict()` de los objetos.
- **TXT**: Genera tickets de salida detallados cada vez que se confirma un pedido.

### 3. Manejo de Excepciones

Se han definido excepciones personalizadas para controlar errores lógicos del negocio sin interrumpir la ejecución del programa:

- **SinStockError**: Se lanza cuando un usuario intenta retirar una cantidad superior a la disponible en el almacén.
- **DatabaseError**: Gestiona fallos en la conexión o ejecución de consultas SQL.

## Flujo de Trabajo del Sistema

### Proceso de Salida de Productos

El proceso garantiza la integridad de los datos mediante los siguientes pasos:

1. **Validación**: El sistema comprueba la existencia del ID y la disponibilidad de stock en el diccionario `inventario_memoria`.
2. **Preparación**: Los productos se añaden temporalmente a una lista de preparación.
3. **Confirmación**: Al confirmar, el sistema actualiza el stock en la base de datos, registra el movimiento y genera el archivo TXT.
```python
def preparar_salida(self, id_prod, cantidad):
    if id_prod not in self.inventario_memoria:
        print("Error: El producto no existe.")
        return
    # Validación de stock mediante excepción personalizada
    if self.inventario_memoria[id_prod].stock < cantidad:
        raise SinStockError(juego.nombre, cantidad, juego.stock)
```

## Requisitos y Configuración

El sistema requiere **Python 3.x** y utiliza la librería estándar `sqlite3`.

Los datos se almacenan en la siguiente jerarquía de directorios:

- `data/almacen.db`: Archivo de base de datos.
- `data/tickets/`: Almacén de tickets generados en formato texto.
- `data/backups/`: Ubicación de los archivos de exportación JSON.

### Instalación y Ejecución

Para iniciar el sistema:
```bash
python Main.py
```

**Credenciales de administrador por defecto:**

- Usuario: `admin`
- Contraseña: `1234`



# Diagrama de Clases UML
<img width="1243" height="987" alt="image" src="https://github.com/user-attachments/assets/440a8239-e8f2-4898-9809-53cca9c76a5c" />

# Modelo entidad relacion 
<img width="801" height="550" alt="Untitled" src="https://github.com/user-attachments/assets/3596645b-5272-4de2-88dd-1fcfd55a1f72" />

# Ordinograma
<img width="899" height="1061" alt="image" src="https://github.com/user-attachments/assets/04d62312-c872-4302-b806-ea3a35c4d938" />
