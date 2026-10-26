from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crear_usuario", methods=["POST"])

def crear_usuario():
    if not Usuario.validar_registro(request.form):
        flash("usuario invalido", "register")
        return redirect("/")

    pass_hasheado = bcrypt.generate_password_hash(request.form['password'])

    datos_registro = {**request.form, 'password': pass_hasheado}

    nuevo_id = Usuario.save(datos_registro)

    session['usuario_id'] = nuevo_id

    return redirect("/dashboard")

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    #buscamos al usuario por su email
    usuario = Usuario.get_by_email({'email': request.form['email_inicio_sesion']})

    #si no existe o la contraseña no coincide, mostramos el mismo mensaje
    if not usuario or not bcrypt.check_password_hash(usuario.password, request.form['password_inicio_sesion']):
        flash("E-mail o contraseña incorrectos", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/dashboard')

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        print("usuario no registrado o iniciado")
        return redirect("/")
    usuario = Usuario.get_one({"id": session["usuario_id"]})
    if not usuario:
        print("usuario no registrado o iniciado")
        return redirect("/")

    misiones = Mision.ver_todos()
        
    return render_template("dashboard.html", usuario=usuario, misiones=misiones)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
