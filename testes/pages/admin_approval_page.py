from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdminApprovalPage:
    def __init__(self, driver):
        self.driver = driver
        self.company_row = (By.XPATH, "//tr[contains(., '{}')]")
        self.approve_button = (By.XPATH, "//button[contains(text(), 'Aprovar')]")
        self.reject_button = (By.XPATH, "//button[contains(text(), 'Rejeitar') or contains(text(), 'Reprovar')]")
        self.details_button = (By.XPATH, "//a[contains(text(), 'Detalhes') or contains(@class, 'btn-info')]")

    def buscar_empresa(self, nome_empresa):
        """Espera a empresa aparecer na lista de pendentes"""
        xpath_empresa = self.company_row[1].format(nome_empresa)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath_empresa))
            )
            return True
        except:
            return False

    def ver_detalhes(self, nome_empresa):
        """Clica em detalhes para validar dados (CT-034-03)"""
        xpath_detalhes = self.company_row[1].format(nome_empresa) + self.details_button[1]
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_detalhes))).click()

    def aprovar_empresa(self, nome_empresa):
        """Aprova a empresa (CT-034-01)"""
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.approve_button))
        btn.click()

        WebDriverWait(self.driver, 10).until(EC.staleness_of(btn))

    def rejeitar_empresa(self, nome_empresa):
        """Rejeita a empresa (CT-034-02)"""
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.reject_button))
        btn.click()
        WebDriverWait(self.driver, 10).until(EC.staleness_of(btn))
