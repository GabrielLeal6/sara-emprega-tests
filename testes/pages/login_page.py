from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost:3000/login" 

    # Puxa pelos Ids o campo
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Ações
    
    def abrir(self):
        self.driver.get(self.url)

    def preencher_email(self, texto):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(texto)

    def preencher_senha(self, texto):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(texto)

    def clicar_entrar(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def obter_valor_email(self):
        return self.driver.find_element(*self.EMAIL_INPUT).get_attribute("value")