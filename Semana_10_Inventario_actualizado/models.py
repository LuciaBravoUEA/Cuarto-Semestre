# Clase Producto
class Producto:
    
    # Constructor: se ejecuta cuando creamos un producto
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Método para obtener los datos en forma de diccionario
    # Esto nos ayuda cuando queremos enviarlo al HTML
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    # Método para mostrar información del producto (útil para consola)
    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio}"
    
    # Clase Inventario
class Inventario:

    def __init__(self):
        # Diccionario para almacenar productos
        # La clave será el ID
        # El valor será el objeto Producto
        self.productos = {}

    # Método para cargar productos desde SQLite al diccionario
    def cargar_desde_db(self, lista_productos):
        for p in lista_productos:
            producto = Producto(p[0], p[1], p[2], p[3])
            self.productos[producto.id] = producto

    # Añadir producto
    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    # Eliminar producto por ID
    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
            return True
        return False

    # Actualizar producto
    def actualizar_producto(self, id, cantidad=None, precio=None):
        if id in self.productos:
            if cantidad is not None:
                self.productos[id].cantidad = cantidad
            if precio is not None:
                self.productos[id].precio = precio
            return True
        return False

    # Buscar producto por nombre
    def buscar_por_nombre(self, nombre):
        resultados = []
        for producto in self.productos.values():
            if nombre.lower() in producto.nombre.lower():
                resultados.append(producto)
        return resultados

    # Mostrar todos los productos
    def mostrar_todos(self):
        return list(self.productos.values())