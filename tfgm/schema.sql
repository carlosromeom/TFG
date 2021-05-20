CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL,
  rol TEXT NOT NULL
);



CREATE TABLE peticiones (
  ID TEXT PRIMARY KEY,
  nombreTrabajo TEXT NOT NULL,
  nombreAlumno TEXT NOT NULL,
  DNI TEXT NOT NULL,
  titulacion TEXT NOT NULL,
  telefonoMovil NUMBER,
  email TEXT  NOT NULL,
  creditosPendientes NUMBER NOT NULL,
  titulo TEXT NOT NULL,
  modificacionAmpliacion BOOLEAN NOT NULL,
  solicitaAdelanto BOOLEAN NOT NULL,
  propuestaTribunal TEXT,
  nombreMiembroTribunal TEXT,
  apellidosMiembroTribunal TEXT,
  DNIMiembroTribunal TEXT,
  emailMiembroTribunal TEXT,
  TitulacionMiembroTribunal TEXT,
  director1 TEXT NOT NULL,
  director1Ext TEXT NOT NULL,
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
  nombre TEXT NOT NULL,
  id NUMBER PRIMARY KEY,
  estado TEXT NOT NULL,
  miembros TEXT NOT NULL,
  presidente TEXT NULL NULL
);



CREATE TABLE tribunal (
  nombre TEXT NOT NULL,
  id NUMBER PRIMARY KEY,
  estado TEXT NOT NULL,
  miembros TEXT NOT NULL,
  presidente TEXT NOT NULL,
  titulacion TEXT NOT NULL
);


CREATE TABLE lectura (
  titulacion TEXT NOT NULL,
  tipoTrabajo TEXT NOT NULL,
  fecha TEXT NOT NULL, 
  hora TEXT NOT NULL,
  alumno TEXT NOT NULL,
  titulo TEXT NOT NULL, 
  aclaraciones TEXT
);