# Aplicación web para la gestión de TFG/M en la EPSC

Proyecto de TFG de Carlos Romeo Muñoz para la gestión de TFG/M en la Escuela Politécnica Superior de Córdoba.
Es una aplicación web desarrollada mediante el microframework Flask donde los Estudiantes podrán subir sus peticiones de tema, sus TFG/M y donde los responsables de la Escuela podrán revisarlos, evaluarlos, etc. Además incluye gestión de comisiones y tribunales de la Escuela, publicación de convocatorias de lectura pública de los trabajos o consulta pública de los trabajos realizados en el pasado por otros alumnos entre otras funciones.

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_Que cosas necesitas para instalar el software y como instalarlas_
En primer lugar es necesaria la instalación del lenguaje de programación Python y el sistema de gestión de paquetes pip:
```
sudo apt-get install python3
sudo apt-get install python3-pip
```
Se incluye un archivo _requrements.txt_ para descargar e instalar las diferentes librerías necesarias de forma sencilla, para ello:

```
python3 -m pip install -r requirements.txt
```

## Despliegue 📦
Una vez instaladas todas las dependencias ya será posible ejecutar la aplicación, para ello se ejecuta el script _runTFGM.sh_ que inicializa el entorno virtual y hace disponible la aplicación para los clientes.


## Construido con 🛠️
El projecto se ha realizado mediante el empleo de las siguientes herramientas:

* [Flask](https://flask.palletsprojects.com/en/2.0.x/) - El framework web empleado
* [Python3](http://python.org) - Lenguaje de programación para el lado del servidor
* [HTML5](https://www.w3.org/html/) - Para la creación de las páginas web que conforman el lado del cliente
* [CSS](https://www.w3.org/Style/CSS/) - Para definir el estilo de las páginas web
* [fpdf](http://www.fpdf.org/) - Librería de Python para crear documentos pdf
* [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) - Protocolo para la conexión a la API de inicio de sesión de Google



## Autores ✒️

* **Carlos Romeo Muñoz** - *Autor del TFG* - [github](https://github.com/carlosromeom)
* **María Luque Rodríguez** - *Directora* 
* **Antonio Arauzo Azofra** - *Director* 

