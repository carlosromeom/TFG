# Python standard libraries
import json
import os
import sqlite3
from datetime import date
from datetime import datetime
from fpdf import FPDF
from flask import make_response
from flask_login import UserMixin

from db import get_db

# Third-party libraries
from flask import Flask, redirect, request, render_template, url_for
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
    if current_user.is_authenticated:
        return render_template('menuprincipal.html')
    else:
        return '<a class="button" href="/login">Google Login</a>'


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
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

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
    
    #introducimos los datos de la plantilla en la base de datos
    #db = get_db()
    #db.execute(
     #       "INSERT INTO peticiones (nombre, direccion, poblacion, codigoPostal, DNI, titulacion, telefonoFijo, telefonoMovil, email, creditosPendientes, titulo, modificacionAmpliacion, solicitaAdelanto, propuestaTribunal, director1, director2, presidente) "
      #      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
       #     (request.form['nombre'], request.form['direccion'], request.form['poblacion'], request.form['codigoPostal'], request.form['DNI'], request.form['titulacion'], request.form['tFijo'], request.form['tMovil'], request.form['email'], request.form['creditosPendientes'], request.form['titulo'], check1, check2, request.form['propuestaTribunal'], request.form['director1'], request.form['director2'], request.form['presidente'])
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

    if request.form.get('solicitaAdelanto'):
        check2="Si"
    else:
        check2="No"



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





# Entregar TFG
@app.route("/entregarTFG", methods=['GET', 'POST'])
def entregarTFG():
    return render_template('entregarTFG.html')

@app.route("/registrarTFG", methods=['GET', 'POST'])
def registrarTFG():
    #introducimos el pdf del TFG en la base de datos

    db = get_db()
    db.execute(
            "INSERT INTO TFGs (trabajo) "
            "VALUES (?)",
            (request.form.get('filename'))
        )

    db.commit()

    return render_template('pantallaOK.html')















if __name__ == "__main__":
    app.run(ssl_context="adhoc")
