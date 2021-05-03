# Python standard libraries
import json
import os
import sqlite3
from datetime import date
from datetime import datetime
from fpdf import FPDF
from flask import make_response
from flask_login import UserMixin
from flask import flash 
from werkzeug.utils import secure_filename

from os import listdir
from os.path import isfile, join


UPLOAD_FOLDER = '/home/carlos/Escritorio/TFG'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



from flask import send_file

from db import get_db

# Third-party libraries
from flask import Flask, redirect, request, render_template, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests



# Internal imports
from db import init_db_command
from user import User


# Configuration
#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_ID = "820618262733-gpag0ppckqsiohe9loeqscduq9jcrlbo.apps.googleusercontent.com"
#GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_CLIENT_SECRET = "rXylh-_s055kBqz_ltF_u6t3"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)






# homepage
@app.route("/")
def index():
   
    if current_user.is_authenticated and (current_user.getRol(session["user_id"])== "Estudiante"):
        return render_template('menuprincipal.html') #En caso de que sea estudiante
    if current_user.is_authenticated and (current_user.getRol(session["user_id"])== "MiembroComision"):
        return render_template('menuprincipalMiembroComision.html') #En caso de que sea miembro de comision
    if current_user.is_authenticated and (current_user.getRol(session["user_id"])== "MiembroTribunal"):
        return render_template('menuprincipalMiembroTribunal.html') #En caso de que sea miembro de tribunal
    if current_user.is_authenticated and (current_user.getRol(session["user_id"])== "MiembroSecretaria"):
        return render_template('menuprincipalMiembroSecretaria.html') #En caso de que sea miembro de secretaria
    else:
        return render_template('inicio.html')


# login
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


# login callback
@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

       # You want to make sure their email is verified.
       # The user authenticated with Google, authorized your
       # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture, rol_="Estudiante"
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture, "Estudiante" )

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))




#presentar peticion de tema
@app.route("/peticion")
def presentarPeticion():
    #return ("hola")
    return render_template('presentarpeticion.html')
      





@app.route("/prepararPDF", methods=['POST'])
def prepararPDF():
    
    

    #return render_template('descargadocumento.html')


    #creamos el documento pdf
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if request.form.get('modificacionAmpliacion'):
        check1="Si"
    else:
        check1="No"

    if request.form.get('solicitaAdelanto'):
        check2="Si"
    else:
        check2="No"


    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute(
            "INSERT INTO peticiones (nombre, direccion, poblacion, codigoPostal, DNI, titulacion, telefonoFijo, telefonoMovil, email, creditosPendientes, titulo, modificacionAmpliacion, solicitaAdelanto, propuestaTribunal, director1, director2, presidente, estado)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (request.form['nombre'], request.form['direccion'], request.form['poblacion'], request.form['codigoPostal'], request.form['DNI'], request.form['titulacion'], request.form['tFijo'], request.form['tMovil'], request.form['email'], request.form['creditosPendientes'], request.form['titulo'], check1, check2, request.form['propuestaTribunal'], request.form['director1'], request.form['director2'], request.form['presidente'], "Creada")
        )

    db.commit()



    pdf.image("https://www.uco.es/eps/images/img/logotipo-EPSC.png", x=135, y=-10, w= 80, h=80 )
    pdf.cell(200, 10, txt="Peticion de tema de TFG", ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="Nombre y apellidos: "+str(request.form['nombre']), ln=2, align="L")
    pdf.cell(200, 10, txt="Direccion: "+str(request.form['direccion']), ln=2, align="L")
    pdf.cell(200, 10, txt="Poblacion: "+str(request.form['poblacion']), ln=2, align="L")
    pdf.cell(200, 10, txt="CP: "+str(request.form['codigoPostal']), ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="DNI: "+str(request.form['DNI']), ln=2, align="L")
    pdf.cell(200, 10, txt="Titulacion: "+str(request.form['titulacion']), ln=2, align="L")
    pdf.cell(200, 10, txt="Telefono fijo: "+str(request.form['tFijo']), ln=2, align="L")
    pdf.cell(200, 10, txt="Telefono movil: "+str(request.form['tMovil']), ln=2, align="L")
    pdf.cell(200, 10, txt="Email: "+str(request.form['email']), ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Creditos pendientes: "+str(request.form['creditosPendientes']), ln=2, align="L")
    pdf.cell(200, 10, txt="El alumno cuyos datos personales han quedado reflejados,", ln=2, align="L")
    pdf.cell(200, 10, txt="Solicita,en virtud de lo dispuesto en la normativa de referencia, la aprobación del Tema para ", ln=2, align="L")
    pdf.cell(200, 10, txt="la realización del Proyecto Fin de Carrera que a continuación se describe, y para la cual se adjunta", ln=2, align="L") 
    pdf.cell(200, 10, txt="documento memoria descriptiva del mismo.", ln=2, align="L")


    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Titulo del proyecto: "+str(request.form['titulo']), ln=2, align="L")
    pdf.cell(200, 10, txt="Modificacion o ampliacion: "+check1, ln=2, align="L")
    pdf.cell(200, 10, txt="Solicita adelanto: "+check2, ln=2, align="L")

    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Propuesta de tribunal: "+str(request.form['propuestaTribunal']), ln=2, align="L")

    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Director 1: "+str(request.form['director1']), ln=2, align="L")
    pdf.cell(200, 10, txt="Director 2: "+str(request.form['director2']), ln=2, align="L")

    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Presidente de la comision de proyectos de: "+str(request.form['presidente']), ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="Peticion creada en: "+str(date.today()), ln=2, align="L")

    pdf.output('peticiondetema', 'F')


    #response = make_response(pdf.output(dest='F').encode('latin-1'))
    #response.headers.set('Content-Disposition', 'attachment', filename="PeticionTema" + '.pdf')
    #response.headers.set('Content-Type', 'application/pdf')




    return render_template('descargadocumento.html')





@app.route('/return-files/')
def return_files_tut():
    try:
        return send_file('/home/carlos/Escritorio/TFG/peticiondetema', attachment_filename='ohhey.pdf')
    except Exception as e:
        return str(e)










# Entregar TFG
@app.route("/subirTFG")
def subirTFG():
    return render_template('subirTFG.html')

@app.route('/registrarTFG', methods=['GET', 'POST'])
def registrarTFG():
    db = get_db()
    db.execute(
    "INSERT INTO TFGs (trabajo, estado, director1, director2, titulacion)"
    "VALUES (?, ?, ?, ?, ?)",
    (request.form['nombre'], 'Creado', request.form['director1'], request.form['director2'], request.form['titulacion'] )
    )
    db.commit()
    return render_template('aux.html')




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #db = get_db()
            #db.execute(
            #"INSERT INTO TFGs (trabajo, estado, director1, director2, titulacion)"
            #"VALUES (?, ?, ?, ?, ?)",
            #(filename, 'Creado', request.form['director1'], request.form['director2'], request.form['titulacion'] )
            #)
            #db.commit()
            return render_template('pantallaOK.html')

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''




#Consultar estado de los tramites

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False




@app.route("/consultarTramites")
def consultarTramites():
    if checkFileExistance("/home/carlos/Escritorio/TFG/peticiondetema") and checkFileExistance("/home/carlos/Escritorio/TFG/TFGCarlos") :
        return render_template('consultarTramitesTodoEntregado.html')
    else:
        return render_template('consultarTramitesSoloPeticion.html')
    






####FUNCIONES PARA EL ACTOR MIEMBRO DE COMISION####

#Consultar peticiones de tema
@app.route("/consultarPeticionesdeTema")
def consultarPeticionesdeTema():
    #lo primero es sacar todas las peticiones de tema de la BD
    db = get_db()
    peticiones=db.execute(
        "SELECT * FROM peticiones where estado = 'Validada'"
        ).fetchall()
   
    #return ("hola")
    return render_template('consultarPeticionesdeTema.html', peticiones=peticiones)


@app.route("/evaluarPeticion/<int:dni>")
def evaluarPeticion(dni):
    return render_template('evaluar.html', dni=dni)

@app.route("/registrarEvaluacion", methods=['GET', 'POST'])
def registrarEvaluacion():
    #return("hola")
    if request.form.get('Aceptada'):
        resolucion="Aceptada"
    if request.form.get('AceptadaSugerencias'):
        resolucion="Aceptada con sugerencias"
    if request.form.get('AmpliarMemoria'):
        resolucion="Ampliar memoria"
    else :
        resolucion="Denegada"

    id=(str(request.form.get('dni')))
    sugerencias= (str(request.form.get('sugerencias')))


  


    #ahora se registra la peticion de tema como evaluada en la BD
    db = get_db()
    db.execute("UPDATE peticiones SET estado='Revisada', resolucion=?, sugerencias=? WHERE DNI= ?", (resolucion, sugerencias, id,),


        )

    db.commit()

    return render_template('pantallaOK.html')



####FUNCIONES PARA EL ACTOR MIEMBRO DE TRIBUNAL####
@app.route("/consultarTrabajosPresentados")
def consultarTrabajosPresentados():
    #lo primero es sacar todos los trabajos sin corregir de la BD

    db = get_db()
    trabajos=db.execute(
        "SELECT * FROM TFGs where estado = 'Validado'"
        ).fetchall()
   
    #return ("hola")
    return render_template('consultarTrabajosPresentados.html', trabajos=trabajos)


@app.route("/intermedio/<nombreTFG>")
def intermedio(nombreTFG):
    return render_template('intermedio.html', nombreTFG=nombreTFG)



@app.route("/returnfiles2/<nombreTFG>")
def returnfiles2(nombreTFG):
    #return(nombreTFG)
    #return(str(nombreTFG))
    try:
        return send_file('/home/carlos/Escritorio/TFG/'+nombreTFG, attachment_filename='ohhey.pdf')
    except Exception as e:
        return str(e)



@app.route('/upload2', methods=['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return render_template('pantallaOK.html')

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
















####FUNCIONES PARA EL ACTOR MIEMBRO DE SECRETARIA####
@app.route("/validarPeticiones")
def validarPeticiones():
    #lo primero es sacar todas las trabajos sin validar de la BD

    db = get_db()
    peticiones=db.execute(
        "SELECT * FROM peticiones where estado = 'Creada'"
        ).fetchall()
   
    #return ("hola")
    return render_template('validarPeticionesdeTema.html', peticiones=peticiones)


@app.route("/validarPeticion/<int:dni>")
def validarPeticion(dni):
    return render_template('validar.html', dni=dni)




@app.route("/registrarValidacion", methods=['GET', 'POST'])
def registrarValidacion():
    #return("hola")
    if request.form.get('Validada'):
        validacion="Validada"
    else :
        validacion="NoValidada"

    id=(str(request.form.get('dni')))
    sugerencias= (str(request.form.get('sugerencias')))


  


    #ahora se registra la peticion de tema como validada o no en la BD
    db = get_db()
    db.execute("UPDATE peticiones SET estado=? WHERE DNI= ?", (validacion, id,),


        )

    db.commit()

    return render_template('pantallaOK.html')







@app.route("/validarTFG")
def validarTFG():
    #lo primero es sacar todos los trabajos sin validar de la BD

    db = get_db()
    trabajos=db.execute(
        "SELECT * FROM TFGs where estado = 'Creado'"
        ).fetchall()
   
    #return ("hola")
    return render_template('validarTrabajos.html', trabajos=trabajos)

@app.route("/registrarValidacionTrabajo/<nombreTFG>")
def registrarValidacionTrabajo(nombreTFG):
    #return("hola")
    return render_template('registrarValidacionTrabajo.html', nombreTFG=nombreTFG)


@app.route("/marcarValidado/<nombreTFG>")
def marcarValidado(nombreTFG):
    #return("hola marcarValidado")

    #ahora lo metemos en la BD como Validado
    db = get_db()
    db.execute("UPDATE TFGs SET estado='Validado' WHERE trabajo= ?", (nombreTFG,),


        )

    db.commit()

    return render_template('pantallaOK.html')







@app.route("/gestionarComisiones")
def gestionarComisiones():
    #lo primero es sacar todas las comisiones ya registradas en la BD

    db = get_db()
    comisiones=db.execute(
        "SELECT * FROM comisiones"
        ).fetchall()
   
    #return ("hola")
    return render_template('gestionarComisiones.html', comisiones=comisiones)



@app.route("/crearComision")
def crearComision():
    #return ("hola crearComision")
    return render_template('crearComision.html')



@app.route("/registrarNuevaComision", methods=['POST'])
def registrarNuevaComision():
    
    #return("hola registrarNuevaComision")

    #return render_template('descargadocumento.html')



    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute(
            "INSERT INTO comisiones (nombre, id, estado, miembros, presidente)"
            "VALUES (?, ?, 'Activa', ?, ?)",
            (request.form['nombre'], request.form['ID'], request.form['miembros'], request.form['presidente'])
        )

    db.commit()
    return render_template('pantallaOK.html')





@app.route("/modificarComision/<int:ID>")
def modificarComision(ID):
    return render_template('modificarComision.html', ID=ID)


@app.route("/cambiarEstadoComision/<int:ID>")
def cambiarEstadoComision(ID):
    return render_template('cambiarEstadoComision.html', ID=ID)


@app.route("/registrarNuevoEstadoComision", methods=['POST'])
def registrarNuevoEstadoComision():
    
    #return("hola registrarNuevaComision")

    #return render_template('descargadocumento.html')


    if request.form.get('Activa'):
        nuevoEstado="Activa"
    else :
        nuevoEstado="Inactiva"


    #return (request.form.get('ID'))

    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute("UPDATE comisiones SET estado=? WHERE ID= ?", (nuevoEstado, request.form.get('ID')),


        )

    db.commit()

    return render_template('pantallaOK.html')







@app.route("/modificarProfesoresComision", methods=['POST'])
def modificarProfesoresComision():
    
    ID=request.form.get('ID')
     #sacamos los miembros de la comision
    db = get_db()
    miembros=db.execute("SELECT miembros FROM comisiones WHERE ID= ?", (ID,),


        ).fetchall()

    return render_template('modificarProfesoresComision.html', ID=ID, miembros=miembros)




    

@app.route("/registrarCambioProfesoresComision", methods=['POST'])
def registrarCambioProfesoresComision():
    return("hola")




















@app.route("/listarTFGTitulacion")
def listarTFGTitulacion():
    return render_template('seleccionarTitulacion.html')






@app.route('/filtrarTitulacion', methods=['GET', 'POST'])
def filtrarTitulacion():
    #return(request.form['titulacion'])


    #ahora guardamos todos los trabajos que sean de la titulacion elegida
    db = get_db()
    trabajos=db.execute(
        "SELECT * FROM TFGs WHERE titulacion= ?", (request.form['titulacion'],),
        ).fetchall()
   
    #return ("hola")
    return render_template('listarTFG.html', trabajos=trabajos)





@app.route("/listarTFGProfesor")
def listarTFGProfesor():
    return render_template('seleccionarProfesor.html')



@app.route('/filtrarProfesor', methods=['GET', 'POST'])
def filtrarProfesor():
    #return(request.form['titulacion'])


    #ahora guardamos todos los trabajos que sean del director elegido
    db = get_db()
    trabajos=db.execute(
        "SELECT * FROM TFGs WHERE director1= ?", (request.form['nombre'],),
        ).fetchall()
   
    #return ("hola")
    return render_template('listarTFG.html', trabajos=trabajos)
















#####FUNCIONES PARA EL USUARIO NO REGISTRADO####################
@app.route("/usuarioNoRegistrado")
def usuarioNoRegistrado():
    return render_template('menuprincipalUsuarioNoRegistrado.html')

@app.route("/filtrado")
def filtrado():
    return render_template('quiereFiltrar.html')


@app.route("/consultarTFG")
def consultarTFG():

    #ahora guardamos todos los trabajos que sean del director elegido
    db = get_db()
    trabajos=db.execute(
        "SELECT * FROM TFGs"
        ).fetchall()
   
    #return ("hola")
    return render_template('listarTFG.html', trabajos=trabajos)


if __name__ == "__main__":
    app.run(ssl_context="adhoc")