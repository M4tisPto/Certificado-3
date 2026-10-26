from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
from datetime import date
BD = "voluntame_esquema"

class Mision:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.fecha = data["fecha"]
        self.voluntarios_necesarios = data["voluntarios_necesarios"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_id = data["usuario_id"]

    @classmethod
    def save(cls, data):
        query = """INSERT INTO misiones (nombre, fecha, voluntarios_necesarios, descripcion, created_at, updated_at, usuario_id)
                VALUES (%(nombre)s, %(fecha)s, %(voluntarios_necesarios)s, %(descripcion)s, NOW(), NOW(), %(usuario_id)s)"""
        return MySQLConnection(BD).query_db(query, data)
    @classmethod
    def ver_todos(cls):
        query = "SELECT * FROM misiones"
        misiones_en_bd = MySQLConnection(BD).query_db(query)
        misiones = []
        for mision in misiones_en_bd:
            misiones.append(cls(mision))
        return misiones

    @classmethod

    def get_one(cls, data):
        query = "SELECT * FROM misiones WHERE id = %(id)s"
        misiones_en_bd = MySQLConnection(BD).query_db(query, data)
        return cls(misiones_en_bd[0])
    @classmethod
    def actualizar(cls, data):
        query = "UPDATE pelicula SET nombre=%(nombre)s, director=%(director)s, fecha_estreno=%(fecha_estreno)s, sinopsis=%(sinopsis)s, usuario_id=%(usuario_id)s, updated_at = NOW() WHERE id = %(id)s"
        return MySQLConnection(BD).query_db(query, data)

    @classmethod
    def borrar(cls, data):
        query = "DELETE FROM peliculas WHERE id = %(id)s;"
        return MySQLConnection(BD).query_db(query,data)
    @staticmethod
    def validar_mision(form):
        is_valid = True
        today = date.today()
        if form["fecha"] < str(today):
            flash("La fecha de inicio no puede ser en el pasado.", "mission")
            is_valid = False
        if 2 <= int(form["voluntarios_necesarios"]) <= 20:
            flash("Los voluntarios necesarios debe ser un número entre 2 y 20.", "mission")
            is_valid = False

        return is_valid