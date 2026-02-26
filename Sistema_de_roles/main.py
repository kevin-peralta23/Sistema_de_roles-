# Importamos las librerías necesarias de Flask
from flask import Flask, render_template, request, redirect, session

# Librerías para generar contraseñas automáticas
import random
import string

# Creamos la aplicación Flask
app = Flask(__name__)

# Clave secreta para manejar sesiones (login)
app.secret_key = "secreto123"

# ROLES DEL SISTEMA

# Lista de roles disponibles en el sistema
roles = ["Administrador", "Maestro", "Alumno"]

# ADMIN POR DEFECTO

# Lista donde se guardan los usuarios del sistema
usuarios = [
    {
        "usuario": "admin",          # Nombre de usuario
        "password": "guadalupe_21",      # Contraseña del admin
        "rol": "Administrador"       # Rol asignado
    }
]

# FUNCION CONTRASEÑA AUTOMATICA

# Función que genera una contraseña aleatoria
def generar_password(longitud=8):
    # Letras mayúsculas, minúsculas y números
    caracteres = string.ascii_letters + string.digits
    
    # Genera una contraseña aleatoria con la longitud indicada
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# LOGIN

# Ruta principal (login)
@app.route("/", methods=["GET", "POST"])
def login():
    
    # Si se envía el formulario (POST)
    if request.method == "POST":
        usuario = request.form["usuario"]   # Obtener usuario del formulario
        password = request.form["password"] # Obtener contraseña del formulario

        # Buscar usuario en la lista
        for u in usuarios:
            if u["usuario"] == usuario and u["password"] == password:
                
                # Guardar datos en sesión
                session["usuario"] = usuario
                session["rol"] = u["rol"]

                # Redirección según el rol
                if u["rol"] == "Administrador":
                    return redirect("/admin")
                elif u["rol"] == "Maestro":
                    return redirect("/maestro")
                elif u["rol"] == "Alumno":
                    return redirect("/alumno")
                else:
                    # Si es un rol nuevo no registrado
                    return redirect("/panel")

        # Si datos incorrectos
        return render_template("login.html", error="Usuario o contraseña incorrecta")

    # Mostrar login si entra normal
    return render_template("login.html")

# PANEL ADMIN

# Ruta del panel del administrador
@app.route("/admin")
def admin():
    
    # Verificar sesión y rol
    if "usuario" not in session or session["rol"] != "Administrador":
        return redirect("/")
    
    # Mostrar panel admin y enviar usuarios y roles al HTML
    return render_template("admin.html", usuarios=usuarios, roles=roles)

# CREAR USUARIO

# Ruta para crear usuarios
@app.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario():
    
    # Solo admin puede entrar
    if "usuario" not in session or session["rol"] != "Administrador":
        return redirect("/")

    # Si se envía el formulario
    if request.method == "POST":
        nuevo_usuario = request.form["usuario"]  # Nombre nuevo usuario
        rol = request.form["rol"]                # Rol seleccionado

        # Generar contraseña automática
        password_generada = generar_password()

        # Guardar usuario en la lista
        usuarios.append({
            "usuario": nuevo_usuario,
            "password": password_generada,
            "rol": rol
        })

        # Mostrar pantalla con datos creados
        return render_template("usuario_creado.html",
                               usuario=nuevo_usuario,
                               password=password_generada,
                               rol=rol)

    # Mostrar formulario crear usuario
    return render_template("crear_usuario.html", roles=roles)

# CREAR ROL NUEVO

# Ruta para crear nuevos roles
@app.route("/crear_rol", methods=["GET", "POST"])
def crear_rol():
    
    # Solo administrador
    if "usuario" not in session or session["rol"] != "Administrador":
        return redirect("/")

    # Si se envía formulario
    if request.method == "POST":
        nuevo_rol = request.form["rol"]  # Nombre del rol nuevo

        # Si no existe, se agrega
        if nuevo_rol not in roles:
            roles.append(nuevo_rol)

        # Regresar al panel admin
        return redirect("/admin")

    # Mostrar formulario crear rol
    return render_template("crear_rol.html")

# PANEL MAESTRO

# Ruta panel maestro
@app.route("/maestro")
def maestro():
    
    # Validar sesión y rol
    if "usuario" not in session or session["rol"] != "Maestro":
        return redirect("/")
    
    # Mostrar panel maestro
    return render_template("maestro.html")

# PANEL ALUMNO

# Ruta panel alumno
@app.route("/alumno")
def alumno():
    
    # Validar sesión y rol
    if "usuario" not in session or session["rol"] != "Alumno":
        return redirect("/")
    
    # Mostrar panel alumno
    return render_template("alumno.html")

#ROLES NUEVOS

# Ruta para roles que no son admin, maestro o alumno
@app.route("/panel")
def panel():
    
    # Verificar que haya sesión activa
    if "usuario" not in session:
        return redirect("/")

    # Mostrar panel genérico
    return render_template("panel.html")

# LOGOUT

# Cerrar sesión
@app.route("/logout")
def logout():
    session.clear()   # Borrar sesión
    return redirect("/")  # Volver al login

# EJECUTAR APP
# Ejecutar servidor Flask
if __name__ == "__main__":
    app.run(debug=True)  # debug=True para modo desarrollo
