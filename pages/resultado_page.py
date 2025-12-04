class ResultadoPage:

    def __init__(self, page):
        self.page = page
    
    def esperar_pdf(self):
        """
        Espera un evento de descarga que ocurre cuando se envía el formulario.
        Retorna el objeto download de Playwright.
        """
        with self.page.expect_download() as download_info:
            self.page.wait_for_load_state("networkidle")
        download = download_info.value
        return download
