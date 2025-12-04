import os

def save_pdf(download, filename="certificado.pdf", folder="output/pdfs"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    ruta = os.path.join(folder, filename)
    download.save_as(ruta)
    return ruta
