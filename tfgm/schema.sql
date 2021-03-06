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
    ("Maria Brox Jimenez", "mbrox", "Profesor"),
    ("David Bullejos Martín", "bullejos", "Profesor"),
    ("Martin Calero Lara", "el1calam", "Profesor"),
    ("Antonio Calvo Cuenca", "acalvo", "Profesor"),
    ("Manuel Cañas Ramirez", "el1caram", "Profesor"),
    ("Juan Francisco Carbonell Márquez", "jcarbonell", "Profesor"),
    ("Angel Carmona Poyato", "ma1capoa", "Profesor"),
    ("Carlos Castillo Rodriguez", "ccastillo", "Profesor"),
    ("Carlos De Castro Lozano", "carlos", "Profesor"),
    ("Rafael Castro Triguero", "me1catrr", "Profesor"),
    ("María Antonia Cejas Molina", "ma1cemom", "Profesor"),
    ("Gonzalo Cerruela Garcia", "in1cegag", "Profesor"),
    ("Arturo Fco. Chica Perez", "iq1chpea", "Profesor"),
    ("Maria Salud Climent Bellido", "qo1clbem", "Profesor"),
    ("Antonio José Cubero Atienza", "ir1cuata", "Profesor"),
    ("Juan Rafael Cubero Atienza", "ir1cuatj", "Profesor"),
    ("Francisca Daza Sánchez", "um1dasaf", "Profesor"),
    ("Maria Del Pilar Dorado Perez", "pilar.dorado", "Profesor"),
    ("Luis Dugo Liébana", "me1dulil", "Profesor"),
    ("Alberto Roberto Espejo Mohedano", "ma1esmor", "Profesor"),
    ("Javier Estevez Gualda", "jestevez", "Profesor"),
    ("Juan Carlos Fernández Caballero", "jfcaballero", "Profesor"),
    ("Luis Manuel Fernández De Ahumada", "in1feahl", "Profesor"),
    ("Nicolás Luis Fernández García", "ma1fegan", "Profesor"),
    ("Jose Maria Flores Arias", "el1flarj", "Profesor"),
    ("Arturo Gallego Segador", "ma1gasea", "Profesor"),
    ("Juan Carlos Gámez Granados", "jcgamez", "Profesor"),
    ("Maria Victoria Garcia Gomez", "me1gagom", "Profesor"),
    ("Laura Garcia Hernandez", "ir1gahel", "Profesor"),
    ("Maria Del Carmen Garcia Martinez", "fa1gamam", "Profesor"),
    ("Carlos Garcia Martínez", "in1gamac", "Profesor"),
    ("Nicolas Emilio Garcia Pedrajas", "npedrajas", "Profesor"),
    ("Enrique García Salcines", "in2gasae", "Profesor"),
    ("Jose Garcia-Aznar Escudero", "el1gaesj", "Profesor"),
    ("José Garres Díaz", "jgarres", "Profesor"),
    ("Juan Luis Garrido Castro", "cc0juanl", "Profesor"),
    ("Juan Garrido Jurado", "p02gajuj", "Profesor"),
    ("Andres Alejandr Gersnoviez Milla", "andresgm", "Profesor"),
    ("Eva Lucrecia Gibaja Galindo", "in1gigae", "Profesor"),
    ("Miguel Angel Gomez Nieto", "mangel", "Profesor"),
    ("Francisco Javier Gómez Uceda", "p12goucf", "Profesor"),
    ("Miguel Jesus Gonzalez Redondo", "el1gorem", "Profesor"),
    ("Guillermo R. Guerrero Vaca", "me1guvag", "Profesor"),
    ("Eduardo Salvador Gutiérrez De Rave Agüera", "ir1gurae", "Profesor"),
    ("Pedro Antonio Gutiérrez Peña", "pagutierrez", "Profesor"),
    ("Jonatan Herrera Fernández", "jherrera", "Profesor"),
    ("Ezequiel Herruzo Gómez", "el1hegoe", "Profesor"),
    ("Francisco José Jiménez Hornero", "ir2jihof", "Profesor"),
    ("Jorge Eugenio Jiménez Hornero", "jjimenez", "Profesor"),
    ("Francisco Javier Jiménez Romero", "p72jirof", "Profesor"),
    ("Francisco Ramón Lara Raya", "el1laraf", "Profesor"),
    ("Josefa Andrea Leva Ramírez", "me1leraj", "Profesor"),
    ("Matías Liñán Reyes", "el1lirem", "Profesor"),
    ("Isabel López García", "qf1lpgai", "Profesor"),
    ("Maria Isabel Lopez Martinez", "q12lomam", "Profesor"),
    ("Antonio Lopez Uceda", "p62louca", "Profesor"),
    ("José María Luna Ariza", "jmluna", "Profesor"),
    ("Juan Jesus Luna Rodríguez", "juan.luna", "Profesor"),
    ("Rafael Luque Álvarez De Sotomayor", "q62alsor", "Profesor"),
    ("María Luque Rodríguez", "in1lurom", "Profesor"),
    ("Irene Telesfora Luque Ruiz", "ma1lurui", "Profesor"),
    ("Francisco Jose Madrid Cuevas", "ma1macuf", "Profesor"),
    ("Alberto Marinas Aramendia", "qo2maara", "Profesor"),
    ("Luis Rafael Martínez Carrillo", "luis.martinez", "Profesor"),
    ("Gonzalo Martínez García", "z42magag", "Profesor"),
    ("Maria Del Pilar Martínez Jiménez", "fa1majip", "Profesor"),
    ("Jose Miguel Martinez Valle", "jmvalle", "Profesor"),
    ("Esteban Meca Álvarez", "ag2meale", "Profesor"),
    ("Juan Carlos Melero Bolaños", "z12meboj", "Profesor"),
    ("Esther Molero Romero", "z72moroe", "Profesor"),
    ("Miguel Angel Montijano Vizcaino", "el1movim", "Profesor"),
    ("Tomas Morales De Luna", "ma1molut", "Profesor"),
    ("Tomas Morales Leal", "el1molet", "Profesor"),
    ("Antonio Moreno Fernandez-Caparros", "el1mofer", "Profesor"),
    ("Carlos Diego Moreno Moreno", "el1momoc", "Profesor"),
    ("Antonio Moreno Muñoz", "amoreno", "Profesor"),
    ("Rafael Muñoz Salinas", "in1musar", "Profesor"),
    ("Joaquín Olivares Bueno", "el1olbuj", "Profesor"),
    ("Jose Luis Olivares Olmedilla", "el1ololj", "Profesor"),
    ("Inés Olmedo Cortés", "qf1olcoi", "Profesor"),
    ("Domingo Ortiz Boyer", "ma1orbod", "Profesor"),
    ("Manuel Agustin Ortiz Lopez", "el1orlom", "Profesor"),
    ("Victor Pallares Lopez", "vpallares", "Profesor"),
    ("Victor Pallares Lopez", "el1palov", "Profesor"),
    ("José Manuel Palomares Muñoz", "el2pamuj", "Profesor"),
    ("José Manuel Palomares Muñoz", "jmpalomares", "Profesor"),
    ("Fernando Peci Lopez", "fernando.peci", "Profesor"),
    ("Gerardo Pedrós Pérez", "fa1pepeg", "Profesor"),
    ("Alberto Jesús Perea Moreno", "g12pemoa", "Profesor"),
    ("Rafael Perez Alcantara", "ir1pealr", "Profesor"),
    ("Sara Pinzi", "qf1pinps", "Profesor"),
    ("Fco. Javier Quiles Latorre", "el1qulaf", "Profesor"),
    ("María Del Carmen Ramos Ordóñez", "carmen.ramos", "Profesor"),
    ("Rafael Jesus Real Calvo", "rafael.real", "Profesor"),
    ("María De Los Dolores Redel Macías", "ig1remam", "Profesor"),
    ("María De Los Dolores Redel Macías", "mredel", "Profesor"),
    ("Alfonso Rider Moyano", "ma1rimoa", "Profesor"),
    ("José Antonio Rivera Reina", "jrivera", "Profesor"),
    ("Oscar Rodríguez Alabanda", "orodriguez", "Profesor"),
    ("Rafael David Rodriguez Cantalejo", "drodriguez", "Profesor"),
    ("Francisco Javier Rodriguez Lozano", "fj.rodriguez", "Profesor"),
    ("Pablo Eduardo Romero Carrillo", "p62rocap", "Profesor"),
    ("Juan Antonio Romero Del Castillo", "aromero", "Profesor"),
    ("Cristóbal Romero Morales", "cromero", "Profesor"),
    ("José Raúl Romero Salguero", "jrromero", "Profesor"),
    ("Rocio Ruiz Bustos", "rrbustos", "Profesor"),
    ("Jorge Ruiz Calviño", "jorgerucal80@gmail.com", "Profesor"),
    ("Manuel María Ruiz De Adana Santiago", "manuel.ruiz", "Profesor"),
    ("José Ruiz García", "el1rugaj", "Profesor"),
    ("Mario Luis Ruz Ruiz", "p12rurum", "Profesor"),
    ("Lorenzo Salas Morera", "lsalas", "Profesor"),
    ("Lorenzo Salas Morera", "mc1samol", "Profesor"),
    ("Elena María Sánchez López", "g02saloe", "Profesor"),
    ("Isabel Pilar Santiago Chiquero", "el1sachi", "Profesor"),
    ("Inmaculada Serrano Gómez", "ma1segoi", "Profesor"),
    ("Rafael Rubén Sola Guirado", "ir2sogur", "Profesor"),
    ("Francisco Táboas Touceda", "qf1tbtof", "Profesor"),
    ("Jesús Pedro Torres Castro", "fa2inte1", "Profesor"),
    ("María Amalia Trillo Holgado", "td1trhom", "Profesor"),
    ("Paula María Triviño Tarradas", "ptrivino", "Profesor"),
    ("Joost Van Duijn", "me2vavaj", "Profesor"),
    ("Francisco J. Vázquez Serrano", "fvazquez", "Profesor"),
    ("Rosalia Villa Jimenez", "z52vijir", "Profesor"),
    ("Enrique Yeguas Bolívar", "in1yeboe", "Profesor"),
    ("Amelia Zafra Gómez", "in1zagoa", "Profesor"),
    ("Jose Zamora Salido", "el1zasaj", "Profesor");

    



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
  localizacion TEXT NOT NULL,
  aclaraciones TEXT 
); 
