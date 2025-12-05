"""teste ct002.01: Fazer logout com sucesso."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuração ---
CHROME_DRIVER_PATH = '/path/to/chromedriver'
PROFILE_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/home/adm'
LOGIN_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/login'

# Credenciais de Teste
VALID_EMAIL = 'fulanoadmnato@sara.com'
VALID_PASSWORD = 'admin123'
WAIT_TIME = 15 

def setup_driver():
    try:
        if CHROME_DRIVER_PATH and CHROME_DRIVER_PATH != '/path/to/chromedriver':
             service = Service(CHROME_DRIVER_PATH)
             driver = webdriver.Chrome(service=service)
        else:
            driver = webdriver.Chrome()
        return driver
    except WebDriverException:
        print("Erro ao configurar o WebDriver. Verifique o caminho do ChromeDriver.")
        return None

def login_to_access_profile(driver):
    
    print("Iniciando Login como pré-requisito...")
    driver.get(LOGIN_URL)
    time.sleep(2)
    
    try:
        # 1. Preenche as credenciais
        email_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        
        email_field.send_keys(VALID_EMAIL)
        password_field.send_keys(VALID_PASSWORD)
        login_button.click()
        
        # 2. Verifica se o login foi para a URL de destino (PROFILE_URL)
        WebDriverWait(driver, WAIT_TIME).until(
            EC.url_to_be(PROFILE_URL)
        )
        time.sleep(2)
        print("Login bem-sucedido. Na área restrita.")
        return True
            
    except TimeoutException:
        print(f"Erro no pré-requisito de Login: Timeout. O login falhou ou não redirecionou para {PROFILE_URL}.")
        return False
    except Exception as e:
        print(f"Erro inesperado no login: {e}")
        return False
        
def test_logout(driver):
    
    # 1. Pré-requisito: Garantir que estamos logados
    if not login_to_access_profile(driver):
        return

    try:
        print("1.  Clicando no ícone do Menu (Hamburger)...")
        menu_button = WebDriverWait(driver, WAIT_TIME).until(
             EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'menu')] | //header//button[1]"))
        )
        menu_button.click()
        time.sleep(2)
        # 2. Clicando na opção 'Sair'
        print("2.  Clicando na opção 'Sair'...")
        logout_link = WebDriverWait(driver, WAIT_TIME).until(
             EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sair') or contains(text(), 'sair')] | //button[contains(text(), 'Sair') or contains(text(), 'sair')]"))
        )
        logout_link.click()
        
        # 3. Verificação: Verifica se o usuário foi redirecionado para a tela de Login
        print("3.  Verificando redirecionamento para a tela de Login...")
        WebDriverWait(driver, WAIT_TIME).until(
            EC.url_to_be(LOGIN_URL)
        )
        
        current_url = driver.current_url
        
        if current_url == LOGIN_URL:
            print(f"\n Teste PASSOU: Logout bem-sucedido. Redirecionado para: {current_url}")
        else:
            print(f"\n Teste FALHOU: O logout pode ter falhado. Permaneceu em: {current_url}")

    except TimeoutException:
         print(f"\n Teste FALHOU: Timeout. O botão de Menu, o link 'Sair' ou a URL de Login não foram encontrados a tempo.")
    except Exception as e:
        print(f"\n Teste FALHOU: Falha inesperada durante o processo de Logout: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_logout(driver)
        finally:
            print("\nTeste concluído. Fechando o navegador em 5 segundos...")
            time.sleep(3)