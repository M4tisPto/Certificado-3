from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision
from flask_app.models.voluntario import Voluntario


@app.route("/registrar_voluntario", methods=["POST"])

def registrar_voluntario():
    data = {**request.form,
        "usuario_id" : session["usuario_id"]
    }

    Voluntario.guardar(data)
    return redirect("/dashboard")


