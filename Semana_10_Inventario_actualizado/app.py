# Importamos librerías necesarias
from flask import Flask, render_template, request, redirect, url_for
from inventario.bd import db
from inventario.productos import Producto
import json
import csv
import os

# Creamos la aplicación Flask
app = Flask(__name__)

# ==============================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==============================

# Indicamos que usaremos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventario.db"

# Desactivamos seguimiento de modificaciones (mejora rendimiento)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializamos la base de datos con la app
db.init_app(app)

# Creamos las tablas automáticamente si no existen
with app.app_context():
    db.create_all()

# ==============================
# RUTAS PRINCIPALES
# ==============================

# Página de inicio
@app.route("/")
def inicio():
    return render_template("index.html")

# Página acerca de
@app.route("/about")
def about():
    return render_template("about.html")

# ==============================
# CRUD CON SQLALCHEMY
# ==============================

# Mostrar inventario completo
@app.route("/inventario")
def inventario():
    # Consultamos todos los productos de la base de datos
    productos = Producto.query.all()
    return render_template("inventario.html", productos=productos)

# Agregar producto
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        # Obtenemos datos del formulario
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        cantidad = int(request.form["cantidad"])

        # Creamos objeto Producto
        nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)

        # Guardamos en la base de datos
        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("inventario"))

    return render_template("agregar.html")

# Eliminar producto
@app.route("/eliminar/<int:id>")
def eliminar(id):
    # Buscamos producto por ID
    producto = Producto.query.get(id)

    if producto:
        db.session.delete(producto)
        db.session.commit()

    return redirect(url_for("inventario"))

# Editar producto
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    producto = Producto.query.get(id)

    if request.method == "POST":
        # Actualizamos atributos
        producto.nombre = request.form["nombre"]
        producto.precio = float(request.form["precio"])
        producto.cantidad = int(request.form["cantidad"])

        db.session.commit()
        return redirect(url_for("inventario"))

    return render_template("editar.html", producto=producto)

# Buscar producto por nombre
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    productos = []

    if request.method == "POST":
        termino = request.form["termino"]

        # Filtro con LIKE
        productos = Producto.query.filter(
            Producto.nombre.like(f"%{termino}%")
        ).all()

    return render_template("buscar.html", productos=productos)

# ==============================
# PERSISTENCIA EN ARCHIVOS
# ==============================

# Guardar datos en TXT
@app.route("/guardar_txt")
def guardar_txt():

    productos = Producto.query.all()

    with open("inventario/data/datos.txt", "w") as f:
        for p in productos:
            f.write(f"{p.id},{p.nombre},{p.cantidad},{p.precio}\n")

    return redirect(url_for("leer_txt"))

# Leer datos TXT
@app.route("/leer_txt")
def leer_txt():

    datos = []

    if os.path.exists("inventario/data/datos.txt"):
        with open("inventario/data/datos.txt", "r") as f:
            datos = f.readlines()

    return render_template("datos.html", datos=datos)


# Guardar datos en JSON
@app.route("/guardar_json")
def guardar_json():

    productos = Producto.query.all()
    data = []

    for p in productos:
        data.append({
            "id": p.id,
            "nombre": p.nombre,
            "cantidad": p.cantidad,
            "precio": p.precio
        })

    with open("inventario/data/datos.json", "w") as f:
        json.dump(data, f, indent=4)

    return redirect(url_for("leer_json"))

# Leer JSON
@app.route("/leer_json")
def leer_json():

    datos = []

    if os.path.exists("inventario/data/datos.json"):
        with open("inventario/data/datos.json", "r") as f:
            datos = json.load(f)

    return render_template("datos.html", datos=datos)


# Guardar datos en CSV
@app.route("/guardar_csv")
def guardar_csv():

    productos = Producto.query.all()

    with open("inventario/data/datos.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # Escribimos encabezados
        writer.writerow(["ID", "Nombre", "Cantidad", "Precio"])

        for p in productos:
            writer.writerow([p.id, p.nombre, p.cantidad, p.precio])

    return redirect(url_for("leer_csv"))

# Leer CSV
@app.route("/leer_csv")
def leer_csv():

    datos = []

    if os.path.exists("inventario/data/datos.csv"):
        with open("inventario/data/datos.csv", "r") as f:
            reader = csv.reader(f)
            datos = list(reader)

    return render_template("datos.html", datos=datos)

# Ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)
    