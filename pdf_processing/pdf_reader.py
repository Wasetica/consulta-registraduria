import pdfplumber

def parse_certificado(path_pdf):
    data = {
        "cedula": None,
        "nombre": None,
        "estado": None,
        "fecha_expedicion": None
    }

    with pdfplumber.open(path_pdf) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

        lines = text.split("\n")

        for linea in lines:
            if "CÉDULA No" in linea.upper():
                data["cedula"] = linea.split(":")[-1].strip()

            if "NOMBRE" in linea.upper():
                data["nombre"] = linea.split(":")[-1].strip()

            if "ESTADO" in linea.upper():
                data["estado"] = linea.split(":")[-1].strip()

            if "EXPEDICIÓN" in linea.upper():
                data["fecha_expedicion"] = linea.split(":")[-1].strip()

    return data
