from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomeAdminPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_empresas_pendentes = (By.LINK_TEXT, "Empresas Pendentes")
        self.logout_btn = (By.XPATH, "//a[contains(text(), 'Sair') or contains(text(), 'Logout')]")
        self.menu_toggle = (By.ID, "menu-toggle")

    def ir_para_aprovacao_empresas(self):
        try:
            toggle = self.driver.find_element(*self.menu_toggle)
            if toggle.is_displayed():
                toggle.click()
        except:
            pass

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.menu_empresas_pendentes)
        ).click()

    def fazer_logout(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.logout_btn)
            ).click()
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/login")
            )
        except:
            print("Erro ao tentar fazer logout ou já deslogado.")
