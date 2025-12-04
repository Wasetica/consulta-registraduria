import time
from utils.captcha_solver import solve_captcha

class ConsultaPage:

    def __init__(self, page):
        self.page = page
        self.url = "https://certvigenciacedula.registraduria.gov.co/Datos.aspx"

        # Selectores reales
        self.cedula_input = "#ContentPlaceHolder1_TextBox1"
        self.dia_select = "#ContentPlaceHolder1_DropDownList1"
        self.mes_select = "#ContentPlaceHolder1_DropDownList2"
        self.anio_select = "#ContentPlaceHolder1_DropDownList3"
        self.captcha_input = "#ContentPlaceHolder1_TextBox2"
        self.captcha_img = "#datos_contentplaceholder1_captcha1_CaptchaImage"
        self.btn_continuar = "#ContentPlaceHolder1_Button1"

    def open(self):
        self.page.goto(self.url, timeout=15000)

    def fill_cedula(self, cedula):
        self.page.fill(self.cedula_input, cedula)

    def fill_fecha(self, dia, mes, anio):
        self.page.select_option(self.dia_select, dia)
        self.page.select_option(self.mes_select, mes)
        self.page.select_option(self.anio_select, anio)

    def solve_and_fill_captcha(self):
        # Capturar imagen CAPTCHA
        self.page.wait_for_selector(self.captcha_img)
        img_bytes = self.page.locator(self.captcha_img).screenshot(path="captcha/temp.png")

        # Resolver CAPTCHA
        resultado = solve_captcha("captcha/temp.png")

        # Llenar CAPTCHA
        self.page.fill(self.captcha_input, resultado)
        return resultado

    def enviar(self):
        self.page.click(self.btn_continuar)
        self.page.wait_for_load_state("networkidle")
