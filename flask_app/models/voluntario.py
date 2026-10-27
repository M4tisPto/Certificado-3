from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
BD = "voluntame_esquema"
class Voluntario:
    def __init__(self, data):
        self.misiones_id = data["mision_id"]
        self.usuarios_id = data["usuario_id"]
        self.nombre_usuario = data.get("nombre_usuario", None)

    @classmethod
    def guardar(cls, data):
        query = "INSERT INTO voluntarios (mision_id, usuario_id) VALUES (%(mision_id)s, %(usuario_id)s)"
        return connectToMySQL(BD).query_db(query, data)
    @classmethod
    def obtener_todos(cls):
        query = "SELECT voluntarios.usuario_id, voluntarios.mision_id, usuarios.nombre AS nombre_usuario, misiones.nombre AS nombre_mision FROM voluntarios JOIN usuarios ON voluntarios.usuario_id = usuarios.id JOIN misiones ON voluntarios.mision_id = misiones.id;"
        
        voluntarios_en_bd = connectToMySQL(BD).query_db(query)

        voluntarios = []
        for voluntario in voluntarios_en_bd:
            voluntarios.append(cls(voluntario))
        return voluntarios