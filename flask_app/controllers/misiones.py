from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision
from flask_app.models.voluntario import Voluntario

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

@app.route("/ver/<int:id>")

def ver_mision(id):
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    data = {
        "id": id
    }
    mision = Mision.get_by_id(data)
    
    voluntarios = Voluntario.obtener_todos()
    return render_template("ver_mision.html", mision = mision, voluntarios = voluntarios)

@app.route("/editar/<int:id>")
def editar_mision(id):
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    data = {
        "id": id
    }
    mision = Mision.get_one(data)
    return render_template("editar_mision.html", mision = mision)
@app.route("/actualizar_mision", methods = ["POST"])
def actualizar_viaje():
    obtener_id = {
        id: request.form['id']
    }
    if not Mision.validar_mision(request.form):
        return redirect(f"/editar/{obtener_id[id]}")
    
    data = {**request.form}
    Mision.actualizar(data)
    return redirect("/dashboard")

@app.route("/borrar/<int:id>")
def borrar_mision(id):
    if "usuario_id" not in session:
        return redirect("/")
    user = Usuario.get_one({"id": session["usuario_id"]})
    if not user:
        return redirect("/")
    data = {
        "id": id
    }
    Mision.borrar(data)
    return redirect("/dashboard")