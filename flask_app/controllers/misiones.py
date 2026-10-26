from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision

@app.route("/nueva")
def nueva_mision():
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    return render_template("nueva_mision.html")

@app.route("/agregar_mision", methods=["POST"])
def agregar_viaje():
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    if not Mision.validar_mision(request.form):
        redirect("/nueva")
    data = {**request.form, "usuario_id": session["usuario_id"]}
    
    Mision.save(data)

    return redirect("/dashboard")
