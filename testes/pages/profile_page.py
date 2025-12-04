from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ProfilePage:
    def __init__(self, driver):
        self.driver = driver
        
        # Locators Visualização
        self.BTN_ATUALIZAR_CRIAR = (By.XPATH, "//button[contains(text(), 'Atualizar') or contains(text(), 'Criar')]")
        self.BTN_EDITAR_DADOS = (By.XPATH, "//button[contains(text(), 'Editar')]")
        
        # Locators Edição
        self.FIELD_NOME = (By.ID, "fullName")
        self.FIELD_TELEFONE = (By.ID, "phoneNumber")
        self.FIELD_EMAIL = (By.ID, "email")
        self.BTN_SALVAR = (By.XPATH, "//button[contains(text(), 'Salvar Currículo')]")
        self.BTN_CANCELAR_EDICAO = (By.XPATH, "//button[contains(text(), 'Cancelar')]")
        
        # Locators Exclusão
        self.BTN_DELETAR_CURRICULO = (By.XPATH, "//button[normalize-space()='Deletar Currículo']")
        self.BTN_CONFIRMAR_DELETE = (By.XPATH, "//button[contains(text(), 'Sim') or contains(text(), 'Confirmar')]")
        
        self.TOAST = (By.CSS_SELECTOR, ".Toastify__toast-body, div[role='alert']")

    # Navegação
    def clicar_editar_ou_criar(self):
        try:
            btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.BTN_ATUALIZAR_CRIAR))
            btn.click()
        except:
            try:
                self.driver.find_element(*self.BTN_EDITAR_DADOS).click()
            except:
                pass 
        
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.BTN_SALVAR))

    # Ações de Formulário
    def preencher_campo(self, campo, valor):
        locators = {"nome": self.FIELD_NOME, "email": self.FIELD_EMAIL, "telefone": self.FIELD_TELEFONE}
        locator = locators[campo]
        
        try:
            element = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(valor)
        except:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].value = arguments[1];", element, valor)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)

    def limpar_campo(self, campo):
        locators = {"nome": self.FIELD_NOME, "email": self.FIELD_EMAIL, "telefone": self.FIELD_TELEFONE}
        locator = locators[campo]
        try:
            element = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(locator))
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.BACKSPACE)
        except:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].value = '';", element)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)

    def obter_valor_campo(self, campo):
        locators = {"nome": self.FIELD_NOME, "email": self.FIELD_EMAIL, "telefone": self.FIELD_TELEFONE}
        return self.driver.find_element(*locators[campo]).get_attribute("value")

    def salvar_alteracoes(self):
        btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.BTN_SALVAR))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.2)
        btn.click()

    def cancelar_edicao(self):
        btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.BTN_CANCELAR_EDICAO))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()

    # Utilitários e Validações
    def lidar_com_alerta(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            texto = alert.text
            alert.accept()
            return texto
        except:
            return None

    def verificar_erro_navegador(self, campo):
        locators = {"nome": self.FIELD_NOME, "email": self.FIELD_EMAIL}
        try:
            return self.driver.find_element(*locators[campo]).get_attribute("validationMessage")
        except:
            return ""

    # Ações de Exclusão
    def clicar_deletar_curriculo(self):
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(self.BTN_DELETAR_CURRICULO)).click()

    def confirmar_exclusao(self):
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(self.BTN_CONFIRMAR_DELETE)).click()

    def cancelar_exclusao_modal(self):
        self.driver.find_element(By.TAG_NAME, "body").click()