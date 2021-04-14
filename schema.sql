CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);



CREATE TABLE peticiones (
  nombre TEXT NOT NULL KEY,
  direccion TEXT NOT NULL,
  poblacion TEXT NOT NULL,
  codigoPostal TEXT  NOT NULL,
  DNI TEXT PRIMARY KEY,
  titulacion TEXT NOT NULL,
  telefonoFijo NUMBER,
  telefonoMovil NUMBER,
  email TEXT  NOT NULL,
  creditosPendientes NUMBER NOT NULL,
  titulo TEXT NOT NULL,
  modificacionAmpliacion BOOLEAN NOT NULL,
  solicitaAdelanto BOOLEAN NOT NULL,
  motivosAdelanto TEXT,
  propuestaTribunal TEXT,
  director1 TEXT NOT NULL,
  director2 TEXT,
  presidente TEXT NOT NULL,
  pdf TEXT NOT NULL
);




