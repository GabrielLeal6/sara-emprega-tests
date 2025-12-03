from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        
        # MAPEAMENTO DOS ELEMENTOS
        self.MENU_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Abrir menu']")
        
        # O link de sair está dentro da navegação e contém o texto "Sair"
        self.LOGOUT_LINK = (By.XPATH, "//nav//a[contains(., 'Sair')]")

    # AÇÕES

    def fazer_logout(self):
        # 1. Clicar no botão do menu para abrir a sidebar
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.MENU_BUTTON)
        ).click()
        
        # 2. Esperar a sidebar abrir e o botão "Sair" ficar visível, depois clicar
        logout_btn = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.LOGOUT_LINK)
        )
        logout_btn.click()

    # NAVEGAÇÃO FORÇADA (Para o CT-002.02)
    def tentar_acessar_home_diretamente(self):

        base_url = self.driver.current_url.split('/login')[0]
        url_restrita = "https://sara-frontend-736daffd516a.herokuapp.com/home/user" 
        self.driver.get(url_restrita)