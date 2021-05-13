# Python standard library
import json
import os
import sqlite3
from datetime import date
from datetime import datetime
from os import listdir
from os.path import isfile, join
import datetime

# Flask modules
from flask import make_response
from flask import flash 
from flask import send_file
from flask import Flask, redirect, request, render_template, url_for, session
from flask_login import UserMixin
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.utils import secure_filename

# Third-party modules
from fpdf import FPDF
from db import get_db
from db import init_db_command

from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from user import User

# Configuration
#GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_ID = "820618262733-gpag0ppckqsiohe9loeqscduq9jcrlbo.apps.googleusercontent.com"
#GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_CLIENT_SECRET = "rXylh-_s055kBqz_ltF_u6t3"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

UPLOAD_FOLDER = '/home/carlos/Escritorio/TFG'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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



# Homepage
@app.route("/")
def index():
    print(current_user)
    if current_user.is_authenticated:
        print(current_user.rol)
        if current_user.rol == "Estudiante":
            return render_template('menuprincipal.html') #En caso de que sea estudiante
        if current_user.rol == "MiembroComision":
            return render_template('menuprincipalMiembroComision.html') #En caso de que sea miembro de comision
        if current_user.rol == "MiembroTribunal":
            return render_template('menuprincipalMiembroTribunal.html') #En caso de que sea miembro de tribunal
        if current_user.rol == "MiembroSecretaria":
            return render_template('menuprincipalMiembroSecretaria.html') #En caso de que sea miembro de secretaria
    else:
        return render_template('inicio.html')



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


    if request.form.get('director1Externo'):
        director1Ext="Si"
    else:
        director1Ext="No"

    if request.form.get('director2Externo'):
        director2Ext="Si"
    else:
        director2Ext="No"


    if request.form.get('creditosPendientes'):
        creditos="Si"
    else:
        creditos="No"
    
    ID = str(current_user.email)+str(datetime.datetime.now())

    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute(
            "INSERT INTO peticiones (ID, nombreTrabajo, nombreAlumno, DNI, titulacion, telefonoMovil, email, creditosPendientes, titulo, modificacionAmpliacion, solicitaAdelanto, propuestaTribunal, nombreMiembroTribunal, apellidosMiembroTribunal, DNIMiembroTribunal, emailMiembroTribunal, TitulacionMiembroTribunal, director1, director1Ext, director2, director2Ext, nombreDirectorExterno, apellidosDirectorExterno, DNIDirectorExterno, emailDirectorExterno, TitulacionDirectorExterno, estado, fecha)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ID, request.form['nombreTrabajo'], request.form['nombreAlumno'], request.form['DNI'], request.form['titulacion'], request.form['tMovil'], current_user.email, creditos, request.form['titulo'], check1, check2, request.form['propuestaTribunal'], request.form['nombreMiembroTribunal'], request.form['apellidosMiembroTribunal'], request.form['DNIMiembroTribunal'], request.form['emailMiembroTribunal'], request.form['TitulacionMiembroTribunal'], request.form['director1'], director1Ext, request.form['director2'], director2Ext, request.form['nombreDirectorExterno'], request.form['apellidosDirectorExterno'], request.form['DNIDirectorExterno'], request.form['emailDirectorExterno'], request.form['TitulacionDirectorExterno'], "Creada", str(datetime.datetime.now()))
        )

    db.commit()




    pdf.image("https://www.uco.es/eps/images/img/logotipo-EPSC.png", x=135, y=-10, w= 80, h=80 )
    pdf.cell(200, 10, txt="Peticion de tema de TFG", ln=1, align="C")
    pdf.cell(200, 10, txt="ID: "+ID, ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="Nombre del trabajo: "+str(request.form['nombreTrabajo']), ln=2, align="L")
    pdf.cell(200, 10, txt="Nombre y apellidos: "+str(request.form['nombreAlumno']), ln=2, align="L")

    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="DNI: "+str(request.form['DNI']), ln=2, align="L")
    pdf.cell(200, 10, txt="Titulacion: "+str(request.form['titulacion']), ln=2, align="L")
    pdf.cell(200, 10, txt="Telefono movil: "+str(request.form['tMovil']), ln=2, align="L")
    pdf.cell(200, 10, txt="Email: "+str(current_user.email), ln=2, align="L")
    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Confirmo cumplimiento requisito creditos pendientes EPSC: "+creditos, ln=2, align="L")
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
    pdf.cell(200, 10, txt="Nombre miembro tribunal: "+str(request.form['nombreMiembroTribunal']), ln=2, align="L")
    pdf.cell(200, 10, txt="Apellidos miembro tribunal: "+str(request.form['apellidosMiembroTribunal']), ln=2, align="L")
    pdf.cell(200, 10, txt="DNI miembro de tribunal: "+str(request.form['DNIMiembroTribunal']), ln=2, align="L")
    pdf.cell(200, 10, txt="Email miembro de tribunal: "+str(request.form['emailMiembroTribunal']), ln=2, align="L")
    pdf.cell(200, 10, txt="Titulacion miembro de tribunal: "+str(request.form['TitulacionMiembroTribunal']), ln=2, align="L")

    pdf.cell(200, 10, txt="", ln=2, align="L")

    pdf.cell(200, 10, txt="Director 1: "+str(request.form['director1']), ln=2, align="L")
    pdf.cell(200, 10, txt="Director 1 Externo: "+director1Ext, ln=2, align="L")


    pdf.cell(200, 10, txt="Director 2: "+str(request.form['director2']), ln=2, align="L")
    pdf.cell(200, 10, txt="Director 2 Externo: "+director2Ext, ln=2, align="L")

    pdf.cell(200, 10, txt="Nombre director externo: "+str(request.form['nombreDirectorExterno']), ln=2, align="L")
    pdf.cell(200, 10, txt="Apellidos director externo: "+str(request.form['apellidosDirectorExterno']), ln=2, align="L")
    pdf.cell(200, 10, txt="DNI director externo: "+str(request.form['DNIDirectorExterno']), ln=2, align="L")
    pdf.cell(200, 10, txt="Email director externo: "+str(request.form['emailDirectorExterno']), ln=2, align="L")
    pdf.cell(200, 10, txt="Titulacion director externo: "+str(request.form['TitulacionDirectorExterno']), ln=2, align="L")




    pdf.cell(200, 10, txt="", ln=2, align="L")


    pdf.cell(200, 10, txt="", ln=2, align="L")
    pdf.cell(200, 10, txt="Peticion creada en: "+str(date.today()), ln=2, align="L")
    

    #nombrePDF="PeticionTema"+request.form['DNI']+str(datetime.datetime.now())
    pdf.output("peticiondetema", 'F')


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


@app.route('/subirMemoria', methods=['GET', 'POST'])
def subirMemoria():
    return render_template('aux.html')







# Entregar TFG
@app.route("/subirTFG")
def subirTFG():
    #lo primero es sacar todas las peticiones de tema de la BD


    db = get_db()
    peticiones=db.execute(
        "SELECT * FROM peticiones where estado = 'Revisada' and email = ?", (str(current_user.email),),
        ).fetchall()
   
    #return ("hola")
    return render_template('consultarPeticionPresentarTrabajo.html', peticiones=peticiones)



    #return render_template('subirTFG.html')


@app.route("/registrarTFG/<string:id>")
def registrarTFG(id):
    db = get_db()
    aux=db.execute(
        "SELECT * FROM peticiones where ID = ?", (id,),
        ).fetchall()
    #print("AUX PRUEBA: " , aux[0][0])


    #hasta aqui va bien





    db = get_db()
    db.execute(
    "INSERT INTO TFGs (ID, nombre, estado, director1, director2, titulacion)"
    "VALUES (?, ?, ?, ?, ?, ?)",
    (id, aux[0][1], 'Creado', aux[0][17], aux[0][19], aux[0][4])
    )
    db.commit()

    
    db = get_db()
    db.execute("UPDATE peticiones SET estado=? WHERE ID= ?", ('TrabajoSubido', id,),
    )

    db.commit()




    return render_template('aux.html')




"""
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

"""


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




@app.route("/descargarDocumentos")
def descargarDocumentos():
    #primero el usuario elige que tipo de documentos ver
    return render_template('elegirDocumentos.html')


@app.route("/descargarPeticion")
def descargarPeticion():
    db = get_db()
    peticiones=db.execute(
        "SELECT * FROM peticiones WHERE email = ?", (str(current_user.email),),
        ).fetchall()

    return render_template('descargarPeticion.html', peticiones=peticiones)



@app.route("/return-files3/<string:email>")
def return_files3(email):
    #return(email)

    try:
        return send_file(UPLOAD_FOLDER+"/"+email+"PETICION.pdf", attachment_filename='ohhey.pdf')
    except Exception as e:
        return str(e)






@app.route("/descargarTrabajo")
def descargarTrabajo():
    try:
        return send_file(UPLOAD_FOLDER+"/"+str(current_user.email)+"TRABAJO.pdf", attachment_filename='ohhey.pdf')
    except Exception as e:
        return str(e)




@app.route("/cancelarPeticion")
def cancelarPeticion():
    db = get_db()
    peticiones=db.execute(
        "SELECT * FROM peticiones WHERE email = ?", (str(current_user.email),),
        ).fetchall()

    return render_template('cancelarPeticion.html', peticiones=peticiones)


@app.route("/marcarCancelada/<string:id>")
def marcarCancelada(id):
    db = get_db()
    db.execute("UPDATE peticiones SET estado='Cancelada' WHERE ID= ?", (id,),


        )

    db.commit()

    return render_template('pantallaOK.html')









@app.route("/consultarEvaluacionPeticion")
def consultarEvaluacionPeticion():
    db = get_db()
    aceptadas=db.execute(
        "SELECT * FROM peticiones WHERE email = ? and resolucion='Aceptada'", (str(current_user.email),),
        ).fetchall()

    db = get_db()
    denegadas=db.execute(
        "SELECT * FROM peticiones WHERE email = ? and resolucion='Denegada'", (str(current_user.email),),
        ).fetchall()

    db = get_db()
    ampliar=db.execute(
        "SELECT * FROM peticiones WHERE email = ? and resolucion='AmpliarMemoria'", (str(current_user.email),),
        ).fetchall()

    db = get_db()
    sugerencias=db.execute(
        "SELECT * FROM peticiones WHERE email = ? and resolucion='AceptadaSugerencias'", (str(current_user.email),),
        ).fetchall()

    db = get_db()
    resto=db.execute(
        "SELECT * FROM peticiones WHERE email = ? and not resolucion = ('AceptadaSugerencias' or 'AmpliarMemoria' or 'Denegada' or 'Aceptada' or 'sugerenciasAceptadas' or 'sugerenciasDenegadas')", (str(current_user.email),),
        ).fetchall()

    return render_template('consultarEvaluacionPeticion.html', aceptadas=aceptadas, denegadas=denegadas, ampliar=ampliar, sugerencias=sugerencias, resto=resto)



"""
    if checkFileExistance("/home/carlos/Escritorio/TFG/peticiondetema"):
        if (peticiones== "Aceptada"):
            return render_template('peticionAceptada.html')
        if (peticiones== "Denegada"):
            return render_template('peticionDenegada.html')
        if (peticiones== "Ampliar Memoria"):
            return render_template('peticionAmpliar.html')
        if (peticiones== "Aceptada con sugerencias"):
            db = get_db()
            sugerencias=db.execute(
                "SELECT sugerencias FROM peticiones where DNI = METER DNI" # a la espera de sacarlo del login de la uco
            ).fetchall()

            db.commit()
            return render_template('peticionSugerencias.html', sugerencias=sugerencias)
        else:
            return render_template('NoEvaluada.html')
    else:
        return render_template('errorNoEncontrado.html')



"""






@app.route("/revisarSugerencias/<string:id>")
def revisarSugerencias(id):
    db = get_db()
    sugerencias=db.execute(
        "SELECT sugerencias FROM peticiones WHERE ID = ? ", (id,),
        ).fetchall()

    return render_template('marcarSugerencias.html', sugerencias=sugerencias, id=id)





@app.route("/guardarSugerencias", methods=['POST'])
def guardarSugerencias():

    db = get_db()
    db.execute("UPDATE peticiones SET resolucion=? WHERE ID= ?", (request.form['marcarSugerencias'],request.form['id'],),


        )

    db.commit()

    return render_template('pantallaOK.html')











@app.route("/ampliar/<string:id>")
def ampliar(id):
    db = get_db()
    sugerencias=db.execute(
        "SELECT sugerencias FROM peticiones WHERE ID = ? ", (id,),
        ).fetchall()

    return render_template('ampliar.html', sugerencias=sugerencias, id=id)











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
        return send_file('/home/carlos/Escritorio/TFG/'+nombreTFG+".pdf", attachment_filename='ohhey.pdf')
    except Exception as e:
        return str(e)



@app.route('/upload2', methods=['GET', 'POST'])
def upload_file2():
    nombre=request.form.get('nombreTFG')
    db = get_db()
    db.execute("UPDATE TFGs SET estado=? WHERE trabajo= ?", ('Corregido', nombre,),
    )

    db.commit()
    
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


    return render_template('asignarTribunal.html', nombreTFG=nombreTFG)


@app.route("/asignarTribunal", methods=['POST'])
def asignarTribunal():
    
    #return("hola")

    #return render_template('descargadocumento.html')





    #return (request.form.get('trabajo'))

    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute("UPDATE TFGs SET tribunal=? WHERE trabajo= ?", (request.form.get('ID'), request.form.get('trabajo')),


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
    #return(ID)
     #sacamos los miembros de la comision
    db = get_db()
    miembros=db.execute("SELECT miembros FROM comisiones WHERE id= ?", (ID,),


        ).fetchone()[0]

    #return(miembros)
    return render_template('modificarProfesoresComision.html', ID=ID, miembros=miembros)




    

@app.route("/registrarCambioProfesoresComision", methods=['POST'])
def registrarCambioProfesoresComision():
    #return(request.form.get('miembros'))


    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute("UPDATE comisiones SET miembros=? WHERE ID= ?", (request.form.get('miembros'), request.form.get('ID')),


        )

    db.commit()

    return render_template('pantallaOK.html')





















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






@app.route("/crearTribunal")
def crearTribunal():
    #return ("hola crearComision")
    return render_template('crearTribunal.html')


@app.route("/registrarNuevoTribunal", methods=['POST'])
def registrarNuevoTribunal():
    
    #return("hola registrarNuevaComision")

    #return render_template('descargadocumento.html')



    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute(
            "INSERT INTO tribunal (nombre, id, estado, miembros, presidente, titulacion)"
            "VALUES (?, ?, 'Activo', ?, ?, ?)",
            (request.form['nombre'], request.form['ID'], request.form['miembros'], request.form['presidente'], request.form['titulacion'])
        )

    db.commit()
    return render_template('pantallaOK.html')




@app.route("/modificarTribunal")
def modificarTribunal():
    #ahora guardamos todos los tribunales
    db = get_db()
    tribunales=db.execute(
        "SELECT * FROM tribunal"
        ).fetchall()
   
    #return ("hola")
    return render_template('mostrarTribunales.html', tribunales=tribunales)



@app.route("/modificarTribunal2/<int:ID>")
def modificarTribunal2(ID):
    return render_template('modificarTribunal.html', ID=ID)



@app.route("/registrarModificacionTribunal", methods=['POST'])
def registrarModificacionTribunal():
    #return(request.form.get('miembros'))


    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute("DELETE from tribunal WHERE ID= ?", (request.form.get('ID')),


        )


    db.commit()

    db.execute(
            "INSERT INTO tribunal (nombre, id, estado, miembros, presidente, titulacion)"
            "VALUES (?, ?, 'Activo', ?, ?, ?)",
            (request.form['nombre'], request.form['ID'], request.form['miembros'], request.form['presidente'], request.form['titulacion'])
        )
    db.commit()

    return render_template('pantallaOK.html')





@app.route("/publicarConvocatorias")
def publicarConvocatorias():
    #return ("hola crearComision")
    return render_template('crearConvocatoria.html')



@app.route("/registrarNuevaConvocatoria", methods=['POST'])
def registrarNuevaConvocatoria():
    
    #return("hola registrarNuevaComision")

    #return render_template('descargadocumento.html')



    #introducimos los datos de la plantilla en la base de datos
    db = get_db()
    db.execute(
            "INSERT INTO lectura (titulacion, tipoTrabajo, fechainicio, fechafin, aclaraciones)"
            "VALUES (?, ?, ?, ?, ?)",
            (request.form['titulacion'], request.form['trabajo'], request.form['fechainicio'], request.form['fechafin'], request.form['notas'])
        )

    db.commit()
    return render_template('pantallaOK.html')









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
        "SELECT * FROM TFGs WHERE estado = 'Corregido'"
        ).fetchall()
   
    #return ("hola")
    return render_template('listarTFG.html', trabajos=trabajos)





@app.route("/consultarTribunalesTitulacion")
def consultarTribunalesTitulacion():
    return render_template('filtrarTribunalTitulacion.html')


@app.route('/filtrarTitulacion2', methods=['GET', 'POST'])
def filtrarTitulacion2():
    #return(request.form['titulacion'])


    #ahora guardamos todos los tribunales que sean de la titulacion elegida
    db = get_db()
    tribunales=db.execute(
        "SELECT * FROM tribunal WHERE titulacion= ?", (request.form['titulacion'],),
        ).fetchall()
   
    #return ("hola")
    return render_template('listarTribunales.html', tribunales=tribunales)



@app.route("/consultarTribunalesProfesor")
def consultarTribunalesProfesor():
    return render_template('filtrarTribunalProfesor.html')



@app.route('/filtrarProfesor2', methods=['GET', 'POST'])
def filtrarProfesor2():
    #return(request.form['titulacion'])


    #ahora guardamos todos los tribunales en los que se encuentre el profesor
    cadena="%"+request.form['nombre']+"%"
    db = get_db()
    tribunales=db.execute(
        "SELECT * FROM tribunal WHERE miembros LIKE ? ", (cadena,),
        ).fetchall()
   
    #return ("hola")
    return render_template('listarTribunales.html', tribunales=tribunales)




@app.route('/consultarConvocatoriasLectura', methods=['GET', 'POST'])
def consultarConvocatoriasLectura():
    #return(request.form['titulacion'])

    fechaHoy=datetime.datetime.now()
    db = get_db()
    convocatorias=db.execute(
        "SELECT * FROM lectura WHERE date(fechafin) >= ? ", (fechaHoy.strftime("%x"),),
        ).fetchall()
   
    #return ("hola")
    return render_template('listarConvocatorias.html', convocatorias=convocatorias)











if __name__ == "__main__":
    app.run(ssl_context="adhoc")