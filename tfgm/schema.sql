CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  rol TEXT NOT NULL
);


-- Extraidos de jinjaProf y directorio UCO: https://www.uco.es/gestion/virtual/directorio-uco
INSERT INTO user (name, email , rol)
VALUES 
    ("Alma Luisa Albujer Brotons", "aalbujer", "Profesor"),
    ("Antonio Arauzo Azofra", "ir1araza", "Profesor"),
    ("Ana Belén Ariza Villaverde", "g82arvia", "Profesor"),
    ("José Luis Ávila Jiménez", "jlavila", "Profesor"),
    ("Luis Ballesteros Olmo", "ma1baoll", "Profesor"),
    ("Maria Brox Jimenez", "mbrox", "Profesor");
    



CREATE TABLE peticiones (
  ID TEXT PRIMARY KEY,
  nombreTrabajo TEXT NOT NULL,
  nombreAlumno TEXT NOT NULL,
  DNI TEXT NOT NULL,
  titulacion TEXT NOT NULL,
  telefonoMovil NUMBER,
  email TEXT NOT NULL,
  creditosPendientes NUMBER NOT NULL,
  modificacionAmpliacion BOOLEAN,
  propuestaTribunal TEXT,
  nombreMiembroTribunal TEXT,
  apellidosMiembroTribunal TEXT,
  DNIMiembroTribunal TEXT,
  emailMiembroTribunal TEXT,
  TitulacionMiembroTribunal TEXT,
  director1 TEXT NOT NULL,
  director2 TEXT,
  director2Ext TEXT,
  nombreDirectorExterno TEXT,
  apellidosDirectorExterno TEXT,
  DNIDirectorExterno TEXT,
  emailDirectorExterno TEXT,
  TitulacionDirectorExterno TEXT,
  estado TEXT NOT NULL,
  resolucion TEXT,
  sugerencias TEXT,
  fecha TEXT NOT NULL
);


CREATE TABLE TFGs (
  ID TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  estado TEXT NOT NULL,
  director1 TEXT NOT NULL,
  director2 TEXT, 
  titulacion TEXT NOT NULL,
  tribunal NUMBER NULL DEFAULT 0
);






CREATE TABLE comisiones (
  titulacion TEXT PRIMARY KEY,
  estado TEXT NOT NULL,
  profesor1 TEXT NOT NULL,
  profesor2 TEXT NOT NULL,
  profesor3 TEXT NOT NULL,
  presidente TEXT NULL NULL
);



CREATE TABLE tribunal (
  id NUMBER PRIMARY KEY,
  estado TEXT NOT NULL,
  email_presidente TEXT NOT NULL,
  email_secretario TEXT NOT NULL,
  email_vocal TEXT NOT NULL,
  titulacion TEXT NOT NULL
);

--Valores de ejemplo:
INSERT INTO tribunal (id, estado , email_presidente, email_secretario, email_vocal, titulacion)
VALUES 
    (0,"Activo","aalbujer", "ir1araza", "jlavila", "informatica");



CREATE TABLE lectura (
  titulacion TEXT NOT NULL,
  tipoTrabajo TEXT NOT NULL,
  fecha TEXT NOT NULL, 
  hora TEXT NOT NULL,
  alumno TEXT NOT NULL,
  titulo TEXT NOT NULL, 
  aclaraciones TEXT  --localizacion
); 
