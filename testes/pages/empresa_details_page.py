from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class EmpresaDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.nome_label = (By.ID, "view_nome")
        self.cnpj_label = (By.ID, "view_cnpj")
        self.email_label = (By.ID, "view_email")
        self.voltar_btn = (By.XPATH, "//a[contains(text(), 'Voltar')]")

    def obter_dados_apresentados(self):
        """Extrai os dados da tela para comparação"""
        dados = {}
        dados['nome'] = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.nome_label)).text
        dados['cnpj'] = self.driver.find_element(*self.cnpj_label).text
        dados['email'] = self.driver.find_element(*self.email_label).text
        return dados

    def voltar(self):
        self.driver.find_element(*self.voltar_btn).click()
