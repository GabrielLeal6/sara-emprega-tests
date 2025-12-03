from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserRegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.NAME = (By.ID, "name")
        self.EMAIL = (By.ID, "email")
        self.PHONE = (By.ID, "telefone")
        self.ADDR = (By.ID, "endereco")
        self.PASS = (By.ID, "password")
        self.CONFIRM = (By.ID, "confirmPassword")
        self.SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
        self.GLOBAL_ERR = (By.CSS_SELECTOR, ".bg-red-100")
        
        # NOVO LOCATOR: Busca qualquer elemento que contenha o texto exato do título
        self.SUCCESS_TITLE = (By.XPATH, "//*[text()='Cadastro Concluído!']")

    def preencher_e_enviar(self, name, email, telefone, endereco, password, confirmPassword):
        self.driver.find_element(*self.NAME).clear()
        self.driver.find_element(*self.NAME).send_keys(name)
        self.driver.find_element(*self.EMAIL).clear()
        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.driver.find_element(*self.PHONE).clear()
        self.driver.find_element(*self.PHONE).send_keys(telefone)
        self.driver.find_element(*self.ADDR).clear()
        self.driver.find_element(*self.ADDR).send_keys(endereco)
        self.driver.find_element(*self.PASS).clear()
        self.driver.find_element(*self.PASS).send_keys(password)
        self.driver.find_element(*self.CONFIRM).clear()
        self.driver.find_element(*self.CONFIRM).send_keys(confirmPassword)
        self.driver.find_element(*self.SUBMIT).click()

    def obter_erro_campo(self, field_id):
        try:
            xpath = f"//input[@id='{field_id}']/following-sibling::p"
            return WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
        except:
            return None

    def obter_erro_cpf_invalido(self):
        try:
            return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.GLOBAL_ERR)).text
        except:
            return None

    # Procura pelo dialogo de sucesso
    def verificar_sucesso(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SUCCESS_TITLE)
            )
            return True
        except:
            return False