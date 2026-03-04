# Importamos SQLAlchemy
# SQLAlchemy es el ORM que nos permite trabajar con la base de datos
# utilizando clases y objetos en lugar de consultas SQL manuales.
from flask_sqlalchemy import SQLAlchemy

# Creamos la instancia global de la base de datos
# Esta instancia será inicializada en app.py
db = SQLAlchemy()
