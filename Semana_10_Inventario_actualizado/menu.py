from models import Producto, Inventario
import sqlite3

# Función para conectar a la base de datos
def conectar():
    return sqlite3.connect("inventario.db")
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def menu():
    crear_tabla()
    inventario = Inventario()

    while True:
        print("\n===== SISTEMA DE INVENTARIO =====")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                (nombre, cantidad, precio)
            )
            conn.commit()
            conn.close()

            print("Producto añadido correctamente.")

        elif opcion == "2":
            id = int(input("ID del producto a eliminar: "))

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
            conn.commit()
            conn.close()

            print("Producto eliminado.")

        elif opcion == "3":
            id = int(input("ID del producto a actualizar: "))
            cantidad = int(input("Nueva cantidad: "))
            precio = float(input("Nuevo precio: "))

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
                (cantidad, precio, id)
            )
            conn.commit()
            conn.close()

            print("Producto actualizado.")

        elif opcion == "4":
            nombre = input("Nombre a buscar: ")

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM productos WHERE nombre LIKE ?",
                ("%" + nombre + "%",)
            )
            resultados = cursor.fetchall()
            conn.close()

            for r in resultados:
                print(r)

        elif opcion == "5":
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            conn.close()

            for p in productos:
                print(p)

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
     menu()
