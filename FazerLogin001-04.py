"""Teste CT001.04 Fazer Login com E-mail Vazio"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time


# NOTE
CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'http://localhost:3000/login'

# Credenciais (a senha é usada apenas para tentar enviar o formulário)
VALID_PASSWORD = 'senha123'
EXPECTED_ERROR_MESSAGE = 'O campo de e-mail é obrigatório.'

def setup_driver():
    """Inicializa e configura o Selenium WebDriver."""
    try:
        if CHROME_DRIVER_PATH and CHROME_DRIVER_PATH != '/path/to/chromedriver':
             service = Service(CHROME_DRIVER_PATH)
             driver = webdriver.Chrome(service=service)
        else:
            driver = webdriver.Chrome()
        return driver
    except WebDriverException as e:
        print(f"Erro ao configurar o WebDriver: {e}")
        print("Por favor, verifique se o ChromeDriver está instalado e o caminho configurado corretamente.")
        return None

def test_empty_email(driver):
    """
    Simula o login com o campo de e-mail vazio e verifica a mensagem de erro.
    """
    
    print(f"1.  Acessando URL: {LOGIN_URL}")
    driver.get(LOGIN_URL)
    time.sleep(2) 
    
    try:
        # --- 2. Localiza o campo de E-mail e DEIXAR VAZIO ---
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')
        print("2.  Deixando o campo de E-mail vazio.")
        

        # --- 3. Localizar e preencher o campo de Senha ---
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        print(f"3.  Inserindo Senha válida (para tentar forçar a submissão).")
        password_field.send_keys(VALID_PASSWORD)
        
        # --- 4. Localizar e clicar no botão 'Entrar' ---
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        print("4.  Clicando em 'Entrar'...")
        login_button.click()

        # --- 5. Verificação da Mensagem de Erro  ---
        time.sleep(1) # Aguarda um momento para a mensagem de erro aparecer
 
        error_message_element = driver.find_element(By.XPATH, f"//p[contains(text(), '{EXPECTED_ERROR_MESSAGE}')]")
        
        if error_message_element.is_displayed():
            print("\n Teste PASSOU: A mensagem de erro obrigatória foi exibida:")
            print(f"   Mensagem exibida: '{error_message_element.text}'")
            print(f"   Mensagem esperada: '{EXPECTED_ERROR_MESSAGE}'")
        else:
            print("\n Teste FALHOU: O campo de e-mail está vazio, mas a mensagem de erro não foi exibida.")
            
    except NoSuchElementException:
        print("\n Teste FALHOU: Um ou mais elementos necessários (campos ou botão 'Entrar') não foram encontrados na página.")
    except Exception as e:
        print(f"\n Ocorreu um erro inesperado durante o teste: {e}")

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_empty_email(driver)
        finally:
            print("\nTeste concluído. Fechando o navegador em 5 segundos...")
            time.sleep(5)
            driver.quit()