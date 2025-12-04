from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmpresaRegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.nome_input = (By.ID, "nome")
        self.cnpj_input = (By.ID, "cnpj")
        self.email_input = (By.ID, "email")
        self.telefone_input = (By.ID, "telefone")
        self.endereco_input = (By.ID, "endereco")
        self.senha_input = (By.ID, "senha")
        self.confirm_senha_input = (By.ID, "confirmPassword")
        self.biografia_input = (By.ID, "biografia")
        self.links_input = (By.ID, "links")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")

        self.success_msg = (By.XPATH, "//*[contains(text(), 'Solicitação Enviada')]")
        self.btn_ir_login = (By.XPATH, "//a[contains(text(), 'Ir para Login') or contains(text(), 'Voltar')]")

        self.error_msg = (By.CSS_SELECTOR, ".alert-danger, .text-danger, .toast-error")

    def abrir(self, base_url):
        self.driver.get(f"{base_url}/cadastro/empresa")

    def preencher_formulario(self, nome, cnpj, email, telefone, endereco, senha, confirm_senha, bio, link):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.nome_input)).send_keys(nome)
        self.driver.find_element(*self.cnpj_input).send_keys(cnpj)
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.telefone_input).send_keys(telefone)
        self.driver.find_element(*self.endereco_input).send_keys(endereco)
        self.driver.find_element(*self.senha_input).send_keys(senha)
        self.driver.find_element(*self.confirm_senha_input).send_keys(confirm_senha)
        self.driver.find_element(*self.biografia_input).send_keys(bio)
        self.driver.find_element(*self.links_input).send_keys(link)

    def submeter(self):
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit_button))
        self.driver.execute_script("arguments[0].scrollIntoView();", btn)
        btn.click()

    def verificar_sucesso(self):
        """
        Retorna True se:
        1. Apareceu mensagem de sucesso
        2. Apareceu botão de 'Ir para Login'
        3. A URL mudou para /login
        """
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(*self.success_msg) or d.find_elements(*self.btn_ir_login)
            )
            return True
        except:
            if "/login" in self.driver.current_url:
                return True
            return False

    def verificar_erro(self):
        try:
            el = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.error_msg))
            return el.text
        except:
            return None
