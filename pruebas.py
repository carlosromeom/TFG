from fpdf import FPDF
pdf=FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.image("https://www.uco.es/eps/images/img/logotipo-EPSC.png", x=135, y=-10, w= 80, h=80 )
pdf.cell(200, 10, txt="Peticion de tema de TFG", ln=1, align="C")
pdf.cell(200, 10, txt="", ln=2, align="L")
pdf.cell(200, 10, txt="", ln=2, align="L")
pdf.cell(200, 10, txt="", ln=2, align="L")
pdf.cell(200, 10, txt="Nombre y apellidos:", ln=2, align="L")
pdf.cell(200, 10, txt="Direccion:", ln=2, align="L")
pdf.cell(200, 10, txt="Poblacion:", ln=2, align="L")
pdf.cell(200, 10, txt="CP:", ln=2, align="L")
pdf.cell(200, 10, txt="", ln=2, align="L")

pdf.cell(200, 10, txt="DNI:", ln=2, align="L")
pdf.cell(200, 10, txt="Titulacion:", ln=2, align="L")
pdf.cell(200, 10, txt="Telefono fijo:", ln=2, align="L")
pdf.cell(200, 10, txt="Telefono movil:", ln=2, align="L")
pdf.cell(200, 10, txt="Email:", ln=2, align="L")
pdf.cell(200, 10, txt="", ln=2, align="L")

pdf.cell(200, 10, txt="Creditos pendientes:", ln=2, align="L")
pdf.cell(200, 10, txt="El alumno cuyos datos personales han quedado reflejados,", ln=2, align="L")
pdf.cell(200, 10, txt="", ln=2, align="L")
pdf.cell(200, 10, txt="Solicita,en virtud de lo dispuesto en la normativa de referencia, la aprobación del Tema para la realización del Proyecto Fin de Carrera que a continuación se describe, y para la cual se adjunta documento memoria descriptiva del mismo.", ln=2, align="L")


pdf.cell(200, 10, txt="", ln=2, align="L")

pdf.cell(200, 10, txt="Titulo del proyecto:", ln=2, align="L")
pdf.cell(200, 10, txt="Modificacion o ampliacion:", ln=2, align="L")
pdf.cell(200, 10, txt="solicita adelanto:", ln=2, align="L")

pdf.cell(200, 10, txt="", ln=2, align="L")

pdf.cell(200, 10, txt="Propuesta de tribunal: ", ln=2, align="L")

pdf.cell(200, 10, txt="", ln=2, align="L")

pdf.cell(200, 10, txt="Director 1:", ln=2, align="L")
pdf.cell(200, 10, txt="Director 2:", ln=2, align="L")

pdf.cell(200, 10, txt="", ln=2, align="L")

pdf.cell(200, 10, txt="Presidente de la comision de proyectos de: ", ln=2, align="L")


pdf.output("peticion.pdf")