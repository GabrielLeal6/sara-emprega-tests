"""teste ct002.01: Fazer logout com sucesso."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

CHROME_DRIVER_PATH = '/path/to/chromedriver'
PROFILE_URL = 'http://localhost:3000/perfil' # URL da sua página de perfil
LOGIN_URL = 'http://localhost:3000/login' # URL esperada após o logout

# As credenciais são necessárias apenas para acessar a página de perfil primeiro
VALID_EMAIL = 'teste@mail.com'
VALID_PASSWORD = 'senha123'

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
    """Simula o login para chegar à tela de perfil."""
    login_page = 'http://localhost:3000/login'
    driver.get(login_page)
    time.sleep(1)
    
    try:
        # Preenche as credenciais
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        
        email_field.send_keys(VALID_EMAIL)
        password_field.send_keys(VALID_PASSWORD)
        login_button.click()
        time.sleep(3) 
        
        if driver.current_url.startswith(PROFILE_URL.replace('/perfil', '')):
            print("Login bem-sucedido. Acessando página de perfil.")
            return True
        else:
            print("Login falhou. Não foi possível prosseguir para o teste de logout.")
            return False
            
    except NoSuchElementException:
        print("Erro: Elementos da tela de login não encontrados.")
        return False
        
def test_logout(driver):
    
    # 1. Pré-requisito: Garantir que estamos logados e na página de perfil
    if not login_to_access_profile(driver):
        return

    try:
        print("1.  Clicando no ícone do Menu (Hamburger)...")
        # Localiza o ícone de menu, que no seu screenshot é o primeiro elemento à esquerda do logo "SARA"
        # Usando um seletor para um ícone/botão no canto superior esquerdo
        menu_button = driver.find_element(By.CSS_SELECTOR, '.MuiButtonBase-root[aria-label="menu"], button[aria-label="menu"], button svg, a svg:first-child')
        menu_button.click()
        time.sleep(1) # Aguarda o menu abrir

        print("2.  Clicando na opção 'Sair'...")
        # Localiza o botão/link "Sair" (logout) dentro do menu que se abriu.
        # Usa XPath para buscar o texto "Sair" ou "Logout" no menu.
        logout_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Sair')] | //button[contains(text(), 'Sair')] | //*[text()='Sair']")
        logout_link.click()
        time.sleep(3) # Aguarda o redirecionamento

        # 3. Verificação: Verifica se o usuário foi redirecionado para a tela de Login
        current_url = driver.current_url
        
        if current_url.startswith(LOGIN_URL) or 'login' in current_url:
            print(f"\n Teste PASSOU: Logout bem-sucedido. Redirecionado para: {current_url}")
        else:
            print(f"\n Teste FALHOU: O logout pode ter falhado. Permaneceu em: {current_url}")

    except NoSuchElementException:
        print("\n Teste FALHOU: Elementos do Menu ou o link 'Sair' não foram encontrados.")
    except Exception as e:
        print(f"\n Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_logout(driver)
        finally:
            print("\nTeste concluído. Fechando o navegador em 5 segundos...")
            time.sleep(5)
            driver.quit()