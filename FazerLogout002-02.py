"""teste ct002.02: tentar acessar area restrita após logout."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
import time

CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/login' 
RESTRICTED_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/home/user' 

def setup_driver():

    try:
        if CHROME_DRIVER_PATH and CHROME_DRIVER_PATH != '/path/to/chromedriver':
             service = Service(CHROME_DRIVER_PATH)
             driver = webdriver.Chrome(service=service)
        else:
            driver = webdriver.Chrome()
        return driver
    except WebDriverException:
        print("Erro: Verifique a instalação e o caminho do ChromeDriver.")
        return None

def test_unauthenticated_access(driver):
    
    print(f"1.  Tentando acessar a URL restrita diretamente: {RESTRICTED_URL}")
    driver.get(RESTRICTED_URL)
    time.sleep(3)
    
    # 2. Verificação
    current_url = driver.current_url
    
    print(f"2.  URL atual após a tentativa: {current_url}")

    if current_url.startswith(LOGIN_URL) or 'login' in current_url:
        print(f"\n Teste PASSOU: Acesso bloqueado. O usuário foi redirecionado para a tela de Login.")
    elif current_url.startswith(RESTRICTED_URL):
        print(f"\n Teste FALHOU: O acesso à área restrita ({RESTRICTED_URL}) foi permitido sem autenticação.")
    else:
         print(f"\n Teste INCONCLUSIVO: O sistema redirecionou para um URL inesperado: {current_url}.")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_unauthenticated_access(driver)
        finally:
            time.sleep(5)
            driver.quit()