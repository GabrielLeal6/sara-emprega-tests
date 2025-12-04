from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.default_url = "https://sara-frontend-736daffd516a.herokuapp.com/login"

    # ELEMENTOS
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Mensagem de erro global (tarja vermelha no topo - erro de backend)
    GLOBAL_ERROR_MESSAGE = (By.CLASS_NAME, "bg-red-100")

    # Mensagens de erro de validação (texto vermelho abaixo dos campos)
    EMAIL_FIELD_ERROR = (By.XPATH, "//input[@id='email']/following-sibling::p")
    PASSWORD_FIELD_ERROR = (
        By.XPATH,
        "//input[@id='password']/parent::div/following-sibling::p",
    )

    # AÇÕES
    def abrir(self, base_url=None):
        """
        Abre a página de login.
        Se base_url for passado (pelos testes), usa ele. Senão, usa o padrão.
        """
        if base_url:
            self.driver.get(f"{base_url}/login")
        else:
            self.driver.get(self.default_url)

    def fazer_login(self, email, senha):
        email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        email_field.clear()

        if email:
            email_field.send_keys(email)

        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        if senha:
            self.driver.find_element(*self.PASSWORD_INPUT).send_keys(senha)

        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        btn.click()

    # VALIDAÇÕES
    def obter_mensagem_erro_global(self):
        try:
            elemento = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.GLOBAL_ERROR_MESSAGE)
            )
            return elemento.text
        except:
            return None

    def obter_erro_campo_email(self):
        try:
            elemento = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.EMAIL_FIELD_ERROR)
            )
            return elemento.text
        except:
            return None

    def obter_erro_campo_senha(self):
        try:
            elemento = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.PASSWORD_FIELD_ERROR)
            )
            return elemento.text
        except:
            return None

    def esta_na_home(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.url_contains("/home"))
            return True
        except:
            return False

    def esta_na_pagina_login(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.LOGIN_BUTTON)
            )
            return True
        except:
            return False
