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
#import numpy as np

from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from . import user



#manejo de errores
def page_not_found(e):
  return render_template('404.html'), 404

def error500(e):
  return render_template('500.html'), 404


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(400, error500)
    app.config.from_mapping(
        SECRET_KEY='developmentKey241',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')#, silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # User session management setup
    # https://flask-login.readthedocs.io/en/latest
    login_manager = LoginManager()
    login_manager.init_app(app)

    from . import database
    # Naive database setup
    # try:
    #     database.init_db_command()
    # except sqlite3.OperationalError:
    #     # Assume it's already been created
    #     pass

    # OAuth 2 client setup
    client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

    # Flask-Login helper to retrieve a user from our db
    @login_manager.user_loader
    def load_user(user_id):
        return user.User.get(user_id)


    # login
    def get_google_provider_cfg():
        return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()


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
            auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
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
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400

        # Login (or sign and login)
        user_object = user.User.get(unique_id)
        if not user_object:
            user_object = user.User(
                id_=unique_id, name=users_name, email=users_email, rol_="Estudiante"
            )
            user.User.create(user_object)
        login_user(user_object)

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
            if current_user.rol == "Profesor":
                return render_template('menuprincipalProfesor.html') #En caso de que sea un profesor
            
            if current_user.rol == "MiembroSecretaria":
                return render_template('menuprincipalMiembroSecretaria.html') #En caso de que sea miembro de secretaria
        else:
            return render_template('inicio.html')



    #presentar peticion de tema
    @app.route('/peticion')
    def presentarPeticion():
        #sacamos una lista con todos los usuarios profesores registrados
        db = database.get_db()
        profesores=db.execute(
            "SELECT * FROM user where rol = 'Profesor'"
            ).fetchall()
        return render_template('presentarpeticion.html', profesores=profesores)


    @app.route("/prepararPDF", methods=['POST'])
    def prepararPDF():
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
            if not file or not allowed_file(file.filename):
                #return 'XXXXX Dar error tipo de fichero no permitido.'
                flash('Tipo de archivo no permitido, use PDF.')
                return redirect(request.url)
            else:
                id_file = str(current_user.email)+str(datetime.datetime.now())
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER_MEMORIAS'], id_file + 'PETICION.pdf'))
                #db = database.get_db()
                #db.execute(
                #"INSERT INTO TFGs (trabajo, estado, director1, director2, titulacion)"
                #"VALUES (?, ?, ?, ?, ?)",
                #(filename, 'Creado', request.form['director1'], request.form['director2'], request.form['titulacion'] )
                #)
                #db.commit()
                

                #creamos el documento pdf
                pdf=FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                if request.form.get('modificacionAmpliacion'):
                    check1="Si"
                else:
                    check1="No"

                if request.form.get('director2Externo'):
                    director2Ext="Si"
                else:
                    director2Ext="No"


                if request.form.get('creditosPendientes'):
                    creditos="Si"
                else:
                    creditos="No"

                #introducimos los datos de la plantilla en la base de datos
        
                db = database.get_db()
                db.execute(
                        "INSERT INTO peticiones (ID, nombreTrabajo, nombreAlumno, DNI, titulacion, telefonoMovil, email, creditosPendientes, modificacionAmpliacion, nombreMiembroTribunal, apellidosMiembroTribunal, DNIMiembroTribunal, emailMiembroTribunal, TitulacionMiembroTribunal, director1, director2, director2Ext, nombreDirectorExterno, apellidosDirectorExterno, DNIDirectorExterno, emailDirectorExterno, TitulacionDirectorExterno, estado, fecha)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (id_file, request.form['nombreTrabajo'], request.form['nombreAlumno'], request.form['DNI'], request.form['titulacion'], request.form['tMovil'], current_user.email, creditos, check1, request.form['nombreMiembroTribunal'], request.form['apellidosMiembroTribunal'], request.form['DNIMiembroTribunal'], request.form['emailMiembroTribunal'], request.form['TitulacionMiembroTribunal'], request.form['director1'], request.form['director2'], director2Ext, request.form['nombreDirectorExterno'], request.form['apellidosDirectorExterno'], request.form['DNIDirectorExterno'], request.form['emailDirectorExterno'], request.form['TitulacionDirectorExterno'], "Creada", str(datetime.datetime.now()))
                    )

                db.commit()


                #para que aparezca el nombre del director 1 en el pdf lo buscamos en la base de datos
                db = database.get_db()
                nombre=db.execute(
                    "SELECT name FROM user where email = ?", (request.form['director1'],),
                    ).fetchall()

        


                pdf.image("https://www.uco.es/eps/images/img/logotipo-EPSC.png", x=135, y=-10, w= 80, h=80 )
                pdf.cell(200, 10, txt="Resguardo de presentación de petición de tema", ln=1, align="C")
                pdf.cell(200, 10, txt="ID: "+id_file, ln=1, align="L")
                pdf.cell(200, 10, txt="", ln=2, align="L")
                pdf.cell(200, 10, txt="", ln=2, align="L")
                pdf.cell(200, 10, txt="", ln=2, align="L")
                pdf.cell(200, 10, txt="Nombre del trabajo: "+str(request.form['nombreTrabajo']), ln=2, align="L")
                pdf.cell(200, 10, txt="Nombre y apellidos: "+str(request.form['nombreAlumno']), ln=2, align="L")

                pdf.cell(200, 10, txt="", ln=2, align="L")

                pdf.cell(200, 10, txt="DNI: "+str(request.form['DNI']), ln=2, align="L")
                pdf.cell(200, 10, txt="Titulación: "+str(request.form['titulacion']), ln=2, align="L")
                pdf.cell(200, 10, txt="Teléfono móvil: "+str(request.form['tMovil']), ln=2, align="L")
                pdf.cell(200, 10, txt="Email: "+str(current_user.email), ln=2, align="L")
                pdf.cell(200, 10, txt="", ln=2, align="L")

                pdf.cell(200, 10, txt="Confirmo cumplimiento requisito créditos pendientes EPSC: "+creditos, ln=2, align="L")
                pdf.cell(200, 10, txt="El alumno cuyos datos personales han quedado reflejados,", ln=2, align="L")
                pdf.cell(200, 10, txt="Solicita,en virtud de lo dispuesto en la normativa de referencia, la aprobación del tema para ", ln=2, align="L")
                pdf.cell(200, 10, txt="la realización del Proyecto Fin de Carrera que a continuación se describe, y para la cual se adjunta", ln=2, align="L") 
                pdf.cell(200, 10, txt="documento memoria descriptiva del mismo.", ln=2, align="L")

                pdf.cell(200, 10, txt="", ln=2, align="L")


                pdf.cell(200, 10, txt="Modificación o ampliación: "+check1, ln=2, align="L")


                pdf.cell(200, 10, txt="", ln=2, align="L")

                # pdf.cell(200, 10, txt="Propuesta de tribunal: "+str(request.form['propuestaTribunal']), ln=2, align="L")
                pdf.cell(200, 10, txt="Nombre miembro tribunal: "+str(request.form['nombreMiembroTribunal']), ln=2, align="L")
                pdf.cell(200, 10, txt="Apellidos miembro tribunal: "+str(request.form['apellidosMiembroTribunal']), ln=2, align="L")
                pdf.cell(200, 10, txt="DNI miembro de tribunal: "+str(request.form['DNIMiembroTribunal']), ln=2, align="L")
                pdf.cell(200, 10, txt="Email miembro de tribunal: "+str(request.form['emailMiembroTribunal']), ln=2, align="L")
                pdf.cell(200, 10, txt="Titulación miembro de tribunal: "+str(request.form['TitulacionMiembroTribunal']), ln=2, align="L")



                pdf.cell(200, 10, txt="Director 1: "+nombre[0][0]+" - "+str(request.form['director1']), ln=2, align="L")



                pdf.cell(200, 10, txt="Director 2: "+str(request.form['director2']), ln=2, align="L")
                pdf.cell(200, 10, txt="Director 2 Externo: "+director2Ext, ln=2, align="L")

                pdf.cell(200, 10, txt="Nombre director externo: "+str(request.form['nombreDirectorExterno']), ln=2, align="L")
                pdf.cell(200, 10, txt="Apellidos director externo: "+str(request.form['apellidosDirectorExterno']), ln=2, align="L")
                pdf.cell(200, 10, txt="DNI director externo: "+str(request.form['DNIDirectorExterno']), ln=2, align="L")
                pdf.cell(200, 10, txt="Email director externo: "+str(request.form['emailDirectorExterno']), ln=2, align="L")
                pdf.cell(200, 10, txt="Titulación director externo: "+str(request.form['TitulacionDirectorExterno']), ln=2, align="L")


                pdf.cell(200, 10, txt="", ln=2, align="L")
                pdf.cell(200, 10, txt="Peticion creada en: "+str(date.today()), ln=2, align="L")

                # nombrePDF=current_user.email+"ResguardoPeticion.pdf"
                # pdf.output(nombrePDF, 'F')

                response = make_response(pdf.output(dest='S').encode('latin-1'))
                response.headers.set('Content-Disposition', 'attachment', filename="PeticionTema" + '.pdf')
                response.headers.set('Content-Type', 'application/pdf')


                return response #render_template('descargadocumento.html')
                #return render_template('pantallaOK.html'), response

        else:
            return '''No es metodo POST, esto no debería pasar'''






    @app.route('/return-files/')
    def return_files_tut():
        try:
            return send_file(app.config['UPLOAD_FOLDER'] +current_user.email+"PETICIONTEMA", attachment_filename='ohhey.pdf')
        except Exception as e:
            return str(e)


    @app.route('/subirMemoria', methods=['GET', 'POST'])
    def subirMemoria():
        return render_template('aux.html')







    # Entregar TFG
    @app.route("/subirTFG")
    def subirTFG():
        #Se comprueba que no halla subido ya un trabajo anteriormente
                #primero se comprueba que el usuario halla subido un trabajo, para ello se ve si tiene alguna petición con el estado de Trabajo subido
        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and estado = 'TrabajoSubido'", (str(current_user.email),),
            ).fetchone()


        if trabajos!=None:
            return render_template('YaSubido.html')


        #lo primero es sacar todas las peticiones de tema de la BD


        db = database.get_db()
        peticiones=db.execute(
            "SELECT * FROM peticiones where estado = 'Revisada' and resolucion= 'Aceptada' and email = ?", (str(current_user.email),),
            ).fetchall()
    
        #return ("hola")
        return render_template('consultarPeticionPresentarTrabajo.html', peticiones=peticiones)



        #return render_template('subirTFG.html')

    @app.route("/registrarTFG/<string:id>")
    def registrarTFG(id):
        db = database.get_db()
        aux=db.execute(
            "SELECT * FROM peticiones where ID = ?", (id,),
            ).fetchall()
        #print("AUX PRUEBA: " , aux[0][0])


        #hasta aqui va bien





        db = database.get_db()
        db.execute(
        "INSERT INTO TFGs (ID, nombre, estado, director1, director2, titulacion)"
        "VALUES (?, ?, ?, ?, ?, ?)",
        (id, aux[0][1], 'Creado', aux[0][15], aux[0][16], aux[0][4])
        )
        db.commit()

        
        db = database.get_db()
        db.execute("UPDATE peticiones SET estado=? WHERE ID= ?", ('TrabajoSubido', id,),
        )

        db.commit()




        return render_template('aux.html')



    """
    @app.route('/registrarTFG', methods=['GET', 'POST'])
    def registrarTFG():
        db = database.get_db()
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
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
                file.save(os.path.join(app.config['UPLOAD_FOLDER_TRABAJOS'], current_user.email + 'TRABAJO.pdf'))

                #db = database.get_db()
                #db.execute(
                #"INSERT INTO TFGs (trabajo, estado, director1, director2, titulacion)"
                #"VALUES (?, ?, ?, ?, ?)",
                #(filename, 'Creado', request.form['director1'], request.form['director2'], request.form['titulacion'] )
                #)
                #db.commit()
                return render_template('pantallaOK.html')

        return '''
        <!doctype html>
        <title>Subir archivo</title>
        <h1>Subir archivo</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Subir>
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
        db = database.get_db()
        peticiones=db.execute(
            "SELECT * FROM peticiones WHERE email = ?", (str(current_user.email),),
            ).fetchall()

        return render_template('descargarPeticion.html', peticiones=peticiones)



    @app.route("/return-files3/<string:id>")
    def return_files3(id):
        try:
            return send_file(app.config['UPLOAD_FOLDER_MEMORIAS'] + '/' + id + 'PETICION.pdf', attachment_filename='peticionTema.pdf')
        except Exception as e:
            return str(e)






    @app.route("/descargarTrabajo")
    def descargarTrabajo():
        #primero se comprueba que el usuario halla subido un trabajo, para ello se ve si tiene alguna petición con el estado de Trabajo subido
        trabajos="aux"
        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and estado = 'TrabajoSubido'", (str(current_user.email),),
            ).fetchone()

        if trabajos==None:
            return render_template('noTrabajo.html')
        else:
            try:
                return send_file(app.config['UPLOAD_FOLDER_TRABAJOS']+"/"+str(current_user.email)+"TRABAJO.pdf", attachment_filename='trabajo.pdf')
            except Exception as e:
                return str(e)




    @app.route("/cancelarPeticion")
    def cancelarPeticion():
        db = database.get_db()
        peticiones=db.execute(
            "SELECT * FROM peticiones WHERE email = ?", (str(current_user.email),),
            ).fetchall()

        return render_template('cancelarPeticion.html', peticiones=peticiones)


    @app.route("/marcarCancelada/<string:id>")
    def marcarCancelada(id):
        db = database.get_db()
        db.execute("UPDATE peticiones SET estado='Cancelada' WHERE ID= ?", (id,),


            )

        db.commit()

        return render_template('pantallaOK.html')









    @app.route("/consultarEvaluacionPeticion")
    def consultarEvaluacionPeticion():
        db = database.get_db()
        aceptadas=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and resolucion='Aceptada'", (str(current_user.email),),
            ).fetchall()

        db = database.get_db()
        denegadas=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and resolucion='Denegada' or estado='NoValidada' ", (str(current_user.email),),
            ).fetchall()

        db = database.get_db()
        ampliar=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and resolucion='AmpliarMemoria'", (str(current_user.email),),
            ).fetchall()

        db = database.get_db()
        sugerencias=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and resolucion='AceptadaSugerencias' or resolucion='SugerenciasAceptadas' or resolucion='sugerenciasDenegadas'", (str(current_user.email),),
            ).fetchall()

        db = database.get_db()
        resto=db.execute(
            "SELECT * FROM peticiones WHERE email = ? and resolucion  != ('AceptadaSugerencias' or 'AmpliarMemoria' or 'Denegada' or 'Aceptada' or 'sugerenciasAceptadas' or 'sugerenciasDenegadas')", (str(current_user.email),),
            ).fetchall()

        return render_template('consultarEvaluacionPeticion.html', aceptadas=aceptadas, denegadas=denegadas, ampliar=ampliar, sugerencias=sugerencias)#, resto=resto)



    """
        if checkFileExistance("/home/carlos/Escritorio/TFG/peticiondetema"):
            if (peticiones== "Aceptada"):
                return render_template('peticionAceptada.html')
            if (peticiones== "Denegada"):
                return render_template('peticionDenegada.html')
            if (peticiones== "Ampliar Memoria"):
                return render_template('peticionAmpliar.html')
            if (peticiones== "Aceptada con sugerencias"):
                db = database.get_db()
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
        db = database.get_db()
        sugerencias=db.execute(
            "SELECT sugerencias FROM peticiones WHERE ID = ? ", (id,),
            ).fetchall()
        aux=sugerencias[0][0]

        return render_template('marcarSugerencias.html', sugerencias=aux, id=id)





    @app.route("/guardarSugerencias", methods=['POST'])
    def guardarSugerencias():
        if request.form.get('Aceptar')=="Aceptar":
            resolucion="SugerenciasAceptadas"
        if request.form.get('Denegar')=="Denegar":
            resolucion="sugerenciasDenegadas"



        db = database.get_db()
        db.execute("UPDATE peticiones SET resolucion=? WHERE ID= ?", (resolucion,request.form['id'],),


            )

        db.commit()

        return render_template('pantallaOK.html')











    @app.route("/ampliar/<string:id>")
    def ampliar(id):
        db = database.get_db()
        sugerencias=db.execute(
            "SELECT sugerencias FROM peticiones WHERE ID = ? ", (id,),
            ).fetchall()

        return render_template('ampliar.html', sugerencias=sugerencias[0][0], id=id)











    ####FUNCIONES PARA EL ACTOR PROFESOR MIEMBRO DE COMISION####

    #Consultar peticiones de tema
    @app.route("/consultarPeticionesdeTema") #OJO MODIFICAR
    def consultarPeticionesdeTema():
        #lo primero es buscar a que comision pertenece el usuario actual
        db = database.get_db()
        comision=db.execute(
            "SELECT * FROM comisiones where profesor1 = ? or profesor2= ? or profesor3=? or presidente=?", ("aalbujer", "aalbujer", "aalbujer", "aalbujer",), #(current_user.email, current_user.email, current_user.email, current_user.email,),
            ).fetchall()


        #return(comision[0][0])

        #Ahora sacamos todas las peticiones de tema de la BD que correspondan a la comision
        db = database.get_db()
        peticiones=db.execute(
            "SELECT * FROM peticiones where estado = 'Validada' or resolucion='SugerenciasAceptadas' or resolucion='sugerenciasDenegadas' and titulacion= ?", (comision[0][0],),
            ).fetchall()
    
        
        return render_template('consultarPeticionesdeTema.html', peticiones=peticiones)


    @app.route("/evaluarPeticion/<string:id>")
    def evaluarPeticion(id):
        db = database.get_db()
        datos=db.execute(
            "SELECT * FROM peticiones where ID = ?", (id,),
            ).fetchall()

        return render_template('evaluar.html', id=id, datos=datos)



    @app.route("/registrarEvaluacion", methods=['GET', 'POST'])
    def registrarEvaluacion():
        #return("hola")
        if request.form.get('Aceptada')=="Aceptada":
            resolucion="Aceptada"
        if request.form.get('AceptadaSugerencias')=="AceptadaSugerencias":
            resolucion="AceptadaSugerencias"
        if request.form.get('AmpliarMemoria')=="AmpliarMemoria":
            resolucion="AmpliarMemoria"
        if request.form.get('Denegada')=="Denegada":
            resolucion="Denegada"
        

        

        
        sugerencias= (str(request.form.get('sugerencias')))


      
        #return(request.form['id']) #no lo saca

        #ahora se registra la peticion de tema como evaluada en la BD
        db = database.get_db()
        db.execute("UPDATE peticiones SET estado='Revisada', resolucion=?, sugerencias=? WHERE ID= ?", (resolucion, sugerencias, request.form['id'],),


            )

        db.commit()

        return render_template('pantallaOK.html')



    ####FUNCIONES PARA EL ACTOR PROFESOR MIEMBRO DE TRIBUNAL####
    @app.route("/consultarTrabajosPresentados")#MODIFICAR CUANDO SE TENGA EL USUARIO
    def consultarTrabajosPresentados():

        #lo primero es sacar cuales son los tribunales del usuario actual
        db2 = database.get_db()
        tribunales=db2.execute(
            "SELECT * FROM tribunal where email_presidente = ? or email_vocal = ? or email_secretario = ?", ("aalbujer", "aalbujer", "aalbujer",),#(current_user.email, current_user.email, current_user.email,),
            ).fetchall()        

        
       # return(tribunales[0][1])



        #Sacamos todos los trabajos sin corregir de la BD

        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM TFGs where estado = 'Validado' and tribunal = ?", (tribunales[0][0],),
            ).fetchall()
    
        #return ("hola")
        return render_template('consultarTrabajosPresentados.html', trabajos=trabajos)


    @app.route("/intermedio/<id>")
    def intermedio(id):
        return render_template('intermedio.html', id=id)



    @app.route("/returnfiles2/<nombreTFG>")
    def returnfiles2(nombreTFG):
        #return(nombreTFG)
        #return(str(nombreTFG))
        try:
            return send_file('/home/carlos/Escritorio/TFG/'+nombreTFG+".pdf", attachment_filename='ohhey.pdf')
        except Exception as e:
            return str(e)



    @app.route('/upload2', methods=['GET', 'POST'])
    def upload2():

        id = request.form.get('id')
        print(id)
        db = database.get_db()
        db.execute("UPDATE TFGs SET estado=? WHERE ID= ?", ('Corregido', request.form.get('id'),),
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
                id_file = str(id)
                print(id)  ##########################ERROR################################
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER_ACTAS']+ '/' + id_file +'ACTA.pdf'))


            

                return render_template('pantallaOK.html')

        return '''
        <!doctype html>
        <title>Subir Acta</title>
        <h1>Subir acta</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Subir>
        </form>
        '''
















    ###################################FUNCIONES PARA EL ACTOR MIEMBRO DE SECRETARIA######################################
    @app.route("/validarPeticiones")
    def validarPeticiones():

        #Busco la equivalencia nombre y login
        db = database.get_db()
        peticiones=db.execute(
            "SELECT * FROM peticiones, user as u1 WHERE peticiones.director1 == u1.email AND peticiones.estado= 'Creada'"
            ).fetchall()

        #lo primero es sacar todas las peticiones sin validar de la BD

        #db = database.get_db()
        #peticiones=db.execute(
         #   "SELECT * FROM peticiones where estado = 'Creada'"
          #  ).fetchall()
    
        #return ("hola")
        return render_template('validarPeticionesdeTema.html', peticiones=peticiones)


    @app.route("/validarPeticion/<string:id>")
    def validarPeticion(id):

        #Busco la equivalencia nombre y login
        db = database.get_db()
        datos=db.execute(
            "SELECT * FROM peticiones, user as u1 WHERE peticiones.director1 == u1.email AND peticiones.estado= 'Creada' and peticiones.ID = ?", (id,),
            ).fetchall()


        #db = database.get_db()
        #datos=db.execute(
         #   "SELECT * FROM peticiones where ID = ?", (id,),
          #  ).fetchall()
        
        
        return render_template('validar.html', id=id, datos=datos)




    @app.route("/registrarValidacion", methods=['GET', 'POST'])
    def registrarValidacion():
        #return("hola")
        if request.form.get('Validada'):
            validacion="Validada"
        else :
            validacion="NoValidada"

        id=(str(request.form.get('id')))


        #return(id)
        #sugerencias= (str(request.form.get('sugerencias')))


    


        #ahora se registra la peticion de tema como validada o no en la BD
        db = database.get_db()
        db.execute("UPDATE peticiones SET estado=? WHERE ID= ?", (validacion, id,),


            )

        db.commit()

        return render_template('pantallaOK.html')







    @app.route("/validarTFG")
    def validarTFG():
        #lo primero es sacar todos los trabajos sin validar de la BD

        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM TFGs where estado = 'Creado'"
            ).fetchall()
    
        #return ("hola")
        return render_template('validarTrabajos.html', trabajos=trabajos)

    @app.route("/registrarValidacionTrabajo/<id>")
    def registrarValidacionTrabajo(id):
        #return("hola")
        return render_template('registrarValidacionTrabajo.html', id=id)


    @app.route("/marcarValidado/<id>")
    def marcarValidado(id):
        #return("hola marcarValidado")

        #ahora lo metemos en la BD como Validado
        db = database.get_db()
        db.execute("UPDATE TFGs SET estado='Validado' WHERE ID= ?", (id,),


            )

        db.commit()

        #Sacamos la titulación del trabajo
        db = database.get_db()
        titulacion=db.execute(
            "SELECT titulacion FROM TFGs WHERE ID= ?", (id,),
            ).fetchall()



        #Sacamos los tribunales de la BD que sean de la misma titulacion que el trabajo
        db = database.get_db()
        tribunales=db.execute(
            "SELECT * FROM tribunal where estado = 'Activo' and titulacion = ?", (titulacion[0][0],),
            ).fetchall()




        return render_template('asignarTribunal.html', id=id, tribunales=tribunales, titulacion=titulacion[0][0])


    @app.route("/asignarTribunal", methods=['POST'])
    def asignarTribunal():
        
        #return("hola")

        #return render_template('descargadocumento.html')



    #####FALLO NO RECIBE EL ID#######

        #return (request.form.get('trabajo'))

        #introducimos los datos de la plantilla en la base de datos
        db = database.get_db()
        db.execute("UPDATE TFGs SET tribunal=? WHERE ID= ?", (request.form.get('tribunal'), request.form.get('trabajo')),


            )

        db.commit()

        return render_template('pantallaOK.html')








    @app.route("/gestionarComisiones") #####FALLO################
    def gestionarComisiones():
        db = database.get_db()
        comisiones=db.execute(
            "SELECT * FROM comisiones, user as u1, user as u2, user as u3, user as u4 WHERE comisiones.profesor1 == u1.email AND comisiones.profesor2 == u2.email AND comisiones.profesor3 == u3.email AND comisiones.presidente == u4.email"
            ).fetchall()

        return render_template('gestionarComisiones.html', comisiones=comisiones)

    '''
        #lo primero es sacar todas las comisiones ya registradas en la BD
        db = database.get_db()
        comisiones=db.execute(
            "SELECT * FROM comisiones"
            ).fetchall()

        #cuento las comisiones
        c=0
        for row in comisiones:
            c=c+1
        #fin del loop
        #return(c)

        matriz = []
        for h in range(9):
            matriz.append([])
            for g in range(c):
                matriz[h].append(None)

        return(matriz[0][0])
        
        i = 0

        for row in comisiones:
            j = 0
            #equivalencia entre id y nombre real
            matriz[i][j]=comisiones[i][0] #titulacion de la comision
            j=j+1
            
            matriz[i][j]=comisiones[i][1]
            j=j+1


            db = database.get_db()
            nombre=db.execute(
                "SELECT name FROM user WHERE email= ?", (comisiones[i][2],),
                ).fetchall()
            matriz[i][j]=comisiones[i][2]
            j=j+1

            matriz[i][j]=nombre[0][0]
            j=j+1


            db = database.get_db()
            nombre2=db.execute(
                "SELECT name FROM user WHERE email= ?", (comisiones[i][3],),
                ).fetchall()
            matriz[i][j]=comisiones[i][3]
            j=j+1

            matriz[i][j]=nombre2[0][0]
            j=j+1

            db = database.get_db()
            nombre3=db.execute(
                "SELECT name FROM user WHERE email= ?", (comisiones[i][4],),
                ).fetchall()
            matriz[i][j]=comisiones[i][4]
            j=j+1

            matriz[i][j]=nombre3[0][0]
            j=j+1

            db = database.get_db()
            nombre4=db.execute(
                "SELECT name FROM user WHERE email= ?", (comisiones[i][5],),
                ).fetchall()
            matriz[i][j]=comisiones[i][5]
            j=j+1

            matriz[i][j]=nombre4[0][0]
            


            i=i+1
            #fin del loop

    
        #return ("hola")
        return render_template('gestionarComisiones.html', matriz=matriz)
    '''


    @app.route("/crearComision")
    def crearComision():
        db = database.get_db()
        profesores=db.execute(
            "SELECT * FROM user WHERE rol= 'Profesor'"
            ).fetchall()

        #return ("hola crearComision")
        return render_template('crearComision.html', profesores=profesores)



    @app.route("/registrarNuevaComision", methods=['POST'])
    def registrarNuevaComision():
        
        #return("hola registrarNuevaComision")

        #return render_template('descargadocumento.html')

        #comprobamos que la comisión no esté repetida
        db = database.get_db()
        comisiones=db.execute(
            "SELECT * FROM comisiones WHERE titulacion = ?", (request.form['titulacion'],),
            ).fetchone()


        if comisiones!=None:
            return render_template('ComisionRepetida.html')




        #introducimos los datos de la plantilla en la base de datos
        db = database.get_db()
        db.execute(
                "INSERT INTO comisiones (titulacion, estado, profesor1, profesor2, profesor3, presidente)"
                "VALUES (?,'Activa', ?, ?, ?, ?)",
                (request.form['titulacion'], request.form['profesor1'], request.form['profesor2'], request.form['profesor3'],  request.form['presidente'])
            )

        db.commit()
        return render_template('pantallaOK.html')





    @app.route("/modificarComision/<string:titulacion>")
    def modificarComision(titulacion):
        return render_template('modificarComision.html', titulacion=titulacion)


    @app.route("/cambiarEstadoComision/<string:titulacion>")
    def cambiarEstadoComision(titulacion):
        return render_template('cambiarEstadoComision.html', titulacion=titulacion)


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
        db = database.get_db()
        db.execute("UPDATE comisiones SET estado=? WHERE titulacion= ?", (nuevoEstado, request.form.get('titulacion')),


            )

        db.commit()

        return render_template('pantallaOK.html')







    @app.route("/modificarProfesoresComision", methods=['POST'])
    def modificarProfesoresComision():
        
        titulacion=request.form.get('titulacion')
        #return(ID)
        #sacamos los miembros de la comision
        db = database.get_db()
        profesor1=db.execute("SELECT profesor1 FROM comisiones WHERE titulacion= ?", (titulacion,),


            ).fetchone()[0]
        profesor2=db.execute("SELECT profesor2 FROM comisiones WHERE titulacion= ?", (titulacion,),


            ).fetchone()[0]
        profesor3=db.execute("SELECT profesor3 FROM comisiones WHERE titulacion= ?", (titulacion,),


            ).fetchone()[0]
        presidente=db.execute("SELECT presidente FROM comisiones WHERE titulacion= ?", (titulacion,),


            ).fetchone()[0]

        #return(miembros)
        return render_template('modificarProfesoresComision.html', titulacion=titulacion, profesor1=profesor1, profesor2=profesor2, profesor3=profesor3, presidente=presidente)




        

    @app.route("/registrarCambioProfesoresComision", methods=['POST'])
    def registrarCambioProfesoresComision():
        #return(request.form.get('miembros'))


        #introducimos los datos de la plantilla en la base de datos
        db = database.get_db()
        db.execute("UPDATE comisiones SET profesor1=?, profesor2=?, profesor3=?, presidente=? WHERE titulacion= ?", (request.form.get('profesor1'), request.form.get('profesor2'), request.form.get('profesor3'), request.form.get('presidente'), request.form.get('titulacion')),


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
        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM TFGs WHERE titulacion= ?", (request.form['titulacion'],),
            ).fetchall()
    
        #return ("hola")
        return render_template('listarTFG.html', trabajos=trabajos)





    @app.route("/listarTFGProfesor")
    def listarTFGProfesor():
    #sacamos la lista de profesores
        db = database.get_db()
        profesores=db.execute(
            "SELECT * FROM user WHERE rol= 'Profesor'"
            ).fetchall()




        return render_template('seleccionarProfesor.html', profesores=profesores)



    @app.route('/filtrarProfesor', methods=['GET', 'POST'])
    def filtrarProfesor():
        #return(request.form['titulacion'])
        #return(request.form['nombre'])
        #return(request.form.get('nombre'))

        #cadena="%"+request.form['nombre']+"%"


        #ahora guardamos todos los trabajos que sean del director elegido
        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM TFGs WHERE director1 LIKE ?", (request.form['nombre'],),
            ).fetchall()
    
        #return ("hola")
        return render_template('listarTFG.html', trabajos=trabajos)






    @app.route("/crearTribunal")
    def crearTribunal():
        #Sacamos el id para el nuevo tribunal

        #cuento los tribunales
        db = database.get_db()
        tribunales=db.execute(
            "SELECT COUNT(*) FROM tribunal"
            ).fetchall()
        #print(trabajos[0][0])


        db = database.get_db()
        profesores=db.execute(
            "SELECT * FROM user WHERE rol= 'Profesor'"
            ).fetchall()

        #return ("hola crearComision")
        return render_template('crearTribunal.html', profesores=profesores, id=tribunales[0][0]+1)






    @app.route("/registrarNuevoTribunal", methods=['POST'])
    def registrarNuevoTribunal():
        #introducimos los datos de la plantilla en la base de datos
        db = database.get_db()
        db.execute(
                "INSERT INTO tribunal (id, estado, email_presidente, email_secretario, email_vocal, titulacion)"
                "VALUES (?,'Activo', ?, ?, ?, ?)",
                (request.form['id'], request.form['presidente'], request.form['secretario'], request.form['vocal'], request.form['titulacion'])
            )

        db.commit()
        return render_template('pantallaOK.html')




    @app.route("/modificarTribunal")
    def modificarTribunal():

        #Busco la equivalencia nombre y login
        db = database.get_db()
        tribunales=db.execute(
            "SELECT * FROM tribunal, user as u1, user as u2, user as u3 WHERE tribunal.email_presidente == u1.email AND tribunal.email_secretario == u2.email AND tribunal.email_vocal == u3.email"
            ).fetchall()

    
        #return ("hola")
        return render_template('mostrarTribunales.html', tribunales=tribunales)



    @app.route("/modificarTribunal2/<int:ID>")
    def modificarTribunal2(ID):
        db = database.get_db()
        datos=db.execute(
            "SELECT * FROM tribunal WHERE id = ?", (ID,),
            ).fetchall()

        db = database.get_db()
        profesores=db.execute(
            "SELECT * FROM user WHERE rol= 'Profesor'"
            ).fetchall()
        return render_template('modificarTribunal.html', ID=ID, datos=datos, profesores=profesores)



    @app.route("/registrarModificacionTribunal", methods=['POST'])
    def registrarModificacionTribunal():
        if request.form.get('Activo'):
            nuevoEstado="Activo"
        else :
            nuevoEstado="Inactivo"


        #introducimos los datos de la plantilla en la base de datos
        db = database.get_db()
        db.execute("DELETE from tribunal WHERE ID= ?", (request.form.get('ID'),),


            )


        db.commit()

        db.execute(
                "INSERT INTO tribunal (id, estado, email_presidente, email_secretario, email_vocal, titulacion)"
                "VALUES (?, ?, ?, ?, ?, ?)",
                (request.form['ID'], nuevoEstado, request.form['presidente'], request.form['secretario'], request.form['vocal'], request.form['titulacion'])
            )
        db.commit()

        return render_template('pantallaOK.html')





    @app.route("/publicarConvocatorias")
    def publicarConvocatorias():
        db = database.get_db()
        trabajos=db.execute(
            "SELECT * FROM TFGs WHERE estado = 'Corregido'"
            ).fetchall()
    
        return render_template('seleccionarTrabajoLectura.html', trabajos=trabajos)

        #return ("hola crearComision")
        #return render_template('crearConvocatoria.html')
        

    @app.route("/datosExtra/<string:id>")
    def datosExtra(id):
        return render_template('crearConvocatoria.html', id=id)




    @app.route("/registrarNuevaConvocatoria", methods=['POST'])
    def registrarNuevaConvocatoria():
        #id=request.form['id']
        #return(id)
        #db = database.get_db()
        #titulacion=db.execute(
        #   "SELECT titulacion FROM peticiones WHERE ID LIKE ?", (id,),
        #  ).fetchall()
        #db.commit()

        
        #return(titulacion[0][0])
        
        #return("hola registrarNuevaComision")

        #return render_template('descargadocumento.html')


        # return(aux[0][4])
        #introducimos los datos de la plantilla en la base de datos
        db = database.get_db()
        db.execute(
                "INSERT INTO lectura (titulacion, tipoTrabajo, fecha, hora, alumno, titulo, localizacion, aclaraciones)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (request.form['titulacion'], request.form['trabajo'], request.form['fecha'], request.form['hora'], request.form['alumno'], request.form['titulo'], request.form['localizacion'], request.form['notas'])
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

        #ahora guardamos todos los trabajos 
        db = database.get_db()
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
        #db = database.get_db()
        #tribunales=db.execute(
         #   "SELECT * FROM tribunal WHERE titulacion= ?", (request.form['titulacion'],),
          #  ).fetchall()

        #Busco la equivalencia nombre y login
        db = database.get_db()
        tribunales=db.execute(
            "SELECT * FROM tribunal, user as u1, user as u2, user as u3 WHERE tribunal.email_presidente == u1.email AND tribunal.email_secretario == u2.email AND tribunal.email_vocal == u3.email AND tribunal.titulacion= ?", (request.form['titulacion'],),
            ).fetchall()

    
        #return ("hola")
        return render_template('listarTribunales.html', tribunales=tribunales)



    @app.route("/consultarTribunalesProfesor")
    def consultarTribunalesProfesor():
        #sacamos la lista de profesores
        db = database.get_db()
        profesores=db.execute(
            "SELECT * FROM user WHERE rol= 'Profesor'"
            ).fetchall()


        return render_template('filtrarTribunalProfesor.html', profesores=profesores)



    @app.route('/filtrarProfesor2', methods=['GET', 'POST'])
    def filtrarProfesor2():
        #return(request.form['titulacion'])


        #ahora guardamos todos los tribunales en los que se encuentre el profesor
        #db = database.get_db()
        #tribunales=db.execute(
         #   "SELECT * FROM tribunal WHERE email_vocal= ? or email_secretario=? or email_presidente=? ", (request.form['nombre'], request.form['nombre'],request.form['nombre'],),
          #  ).fetchall()


        #Busco la equivalencia nombre y login
        db = database.get_db()
        tribunales=db.execute(
            "SELECT * FROM tribunal, user as u1, user as u2, user as u3 WHERE tribunal.email_presidente == u1.email AND tribunal.email_secretario == u2.email AND tribunal.email_vocal == u3.email AND (tribunal.email_secretario= ? or tribunal.email_vocal = ? or tribunal.email_presidente = ?)", (request.form['nombre'], request.form['nombre'],request.form['nombre'],),
            ).fetchall()

    
        #return ("hola")
        return render_template('listarTribunales.html', tribunales=tribunales)




    @app.route('/consultarConvocatoriasLectura', methods=['GET', 'POST'])
    def consultarConvocatoriasLectura():
        #return(request.form['titulacion'])

        fechaHoy=datetime.datetime.now()
        db = database.get_db()
        convocatorias=db.execute(
            "SELECT * FROM lectura WHERE date(fecha) >= ? ", (fechaHoy.strftime("%x"),),
            ).fetchall()
    
        #return ("hola")
        return render_template('listarConvocatorias.html', convocatorias=convocatorias)












    ##################FUNCIONES AUXILIARES##############################3

    @app.route("/descargarTrabajo2/<string:id>")
    def descargarTrabajo2(id):
        
        db = database.get_db()
        email=db.execute(
            "SELECT email FROM peticiones where ID = ?", (id,),
            ).fetchall()

        

        try:
            return send_file(app.config['UPLOAD_FOLDER_TRABAJOS']+"/"+email[0][0]+"TRABAJO.pdf", attachment_filename='trabajo.pdf')
        except Exception as e:
            return str(e)






    return app
