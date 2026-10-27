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
        self.nombre_usuario = data.get("nombre_usuario", None)

    @classmethod
    def save(cls, data):
        query = """INSERT INTO misiones (nombre, fecha, voluntarios_necesarios, descripcion, created_at, updated_at, usuario_id)
                VALUES (%(nombre)s, %(fecha)s, %(voluntarios_necesarios)s, %(descripcion)s, NOW(), NOW(), %(usuario_id)s)"""
        return MySQLConnection(BD).query_db(query, data)
    @classmethod
    def ver_todos(cls):
        query = "SELECT misiones.*, usuarios.nombre AS nombre_usuario FROM misiones LEFT JOIN usuarios ON misiones.usuario_id = usuarios.id"
        misiones_en_bd = MySQLConnection(BD).query_db(query)
        misiones = []
        for mision in misiones_en_bd:
            misiones.append(cls(mision))
        return misiones

    @classmethod
    def get_one(cls, data):
        query = "SELECT misiones.*, usuarios.id AS usuario_id_de_tabla FROM misiones LEFT JOIN usuarios ON misiones.usuario_id = usuarios.id WHERE misiones.id = %(id)s"
        misiones_en_bd = MySQLConnection(BD).query_db(query, data)
        return cls(misiones_en_bd[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT misiones.*, usuarios.nombre AS nombre_usuario FROM misiones LEFT JOIN usuarios ON misiones.usuario_id = usuarios.id WHERE misiones.id = %(id)s"
        misiones_en_bd = MySQLConnection(BD).query_db(query, data)
        return cls(misiones_en_bd[0])
    @classmethod
    def actualizar(cls, data):
        query = """UPDATE misiones 
        SET nombre=%(nombre)s, fecha=%(fecha)s, voluntarios_necesarios=%(voluntarios_necesarios)s, 
        descripcion=%(descripcion)s, usuario_id=%(usuario_id)s, updated_at = NOW() WHERE id = %(id)s"""
        return MySQLConnection(BD).query_db(query, data)

    @classmethod
    def borrar(cls, data):
        query = "DELETE FROM misiones WHERE id = %(id)s;"
        return MySQLConnection(BD).query_db(query,data)
    @staticmethod
    def validar_mision(form):
        is_valid = True
        today = date.today()
        if form["fecha"] < str(today):
            flash("La fecha de inicio no puede ser en el pasado.", "mission")
            is_valid = False
        if 2 > int(form["voluntarios_necesarios"]) or 20 < int(form["voluntarios_necesarios"]):
            flash("Los voluntarios necesarios debe ser un número entre 2 y 20.", "mission")
            is_valid = False

        return is_valid