from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://sara-frontend-736daffd516a.herokuapp.com/login" 

    # ELEMENTOS
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Mensagem de erro global (tarja vermelha no topo - erro de backend)
    GLOBAL_ERROR_MESSAGE = (By.CLASS_NAME, "bg-red-100")

    # Mensagens de erro de validação (texto vermelho abaixo dos campos)
    EMAIL_FIELD_ERROR = (By.XPATH, "//input[@id='email']/following-sibling::p")
    # Para senha, o erro está fora da div relativa do input (devido ao botão de 'olho')
    PASSWORD_FIELD_ERROR = (By.XPATH, "//input[@id='password']/parent::div/following-sibling::p")

    # AÇÕES
    def abrir(self):
        self.driver.get(self.url)

    def fazer_login(self, email, senha):
        self.driver.find_element(*self.EMAIL_INPUT).clear()
        if email: 
            self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        if senha:
            self.driver.find_element(*self.PASSWORD_INPUT).send_keys(senha)
        
        self.driver.find_element(*self.LOGIN_BUTTON).click()

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
            WebDriverWait(self.driver, 5).until(
                EC.url_contains("/home")
            )
            return True
        except:
            return False