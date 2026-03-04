# Importamos la instancia de la base de datos
from .bd import db

# Definimos el modelo Producto
# Este modelo representa la tabla "productos" en la base de datos
class Producto(db.Model):

    # Nombre de la tabla en SQLite
    __tablename__ = "productos"

    # Definimos las columnas de la tabla

    # Clave primaria autoincremental
    id = db.Column(db.Integer, primary_key=True)

    # Nombre del producto (no puede ser nulo)
    nombre = db.Column(db.String(100), nullable=False)

    # Cantidad disponible (no puede ser nula)
    cantidad = db.Column(db.Integer, nullable=False)

    # Precio del producto (tipo decimal)
    precio = db.Column(db.Float, nullable=False)

    # Método de representación del objeto
    # Útil para depuración en consola
    def __repr__(self):
        return f"<Producto {self.nombre}>"