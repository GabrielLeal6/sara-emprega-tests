"""Login CT001.05: Campo de Senha Vazio"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

# --- Configuração ---
# NOTE: Mantenha o caminho do seu ChromeDriver ou use None se estiver no PATH
CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'http://localhost:3000/login' # URL do seu screenshot

# Credenciais e Mensagem de Erro
VALID_EMAIL = 'teste@mail.com'
EXPECTED_ERROR_MESSAGE = 'O campo de senha é obrigatório.'

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

def test_empty_password(driver):
    """
    Simula o login com o campo de senha vazio e verifica a mensagem de erro.
    """
    
    print(f"1. 🚀 Acessando URL: {LOGIN_URL}")
    driver.get(LOGIN_URL)
    time.sleep(2) 
    
    try:
        # --- 2. Localizar e preencher o campo de E-mail ---
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')
        print(f"2. 📧 Inserindo E-mail: {VALID_EMAIL}")
        email_field.send_keys(VALID_EMAIL)
        
        # --- 3. Localizar o campo de Senha e DEIXAR VAZIO ---
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        print("3. 🔑 Deixando o campo de Senha vazio.")
        # Não fazemos nada, o campo já está vazio após o carregamento da página

        # --- 4. Localizar e clicar no botão 'Entrar' ---
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        print("4. 👆 Clicando em 'Entrar'...")
        login_button.click()

        # --- 5. Verificação da Mensagem de Erro (CRUCIAL) ---
        time.sleep(1) # Aguarda um momento para a mensagem de erro aparecer
        
        # Localiza a mensagem de erro específica, que no seu screenshot está sob o campo de Senha.
        # Usamos uma busca por XPath que contém o texto da mensagem esperada.
        # Ajustamos o XPath para buscar a mensagem de erro específica da senha:
        error_message_element = driver.find_element(By.XPATH, f"//p[contains(text(), '{EXPECTED_ERROR_MESSAGE}')]")
        
        if error_message_element.is_displayed():
            print("\n✅ Teste PASSOU: A mensagem de erro obrigatória foi exibida:")
            print(f"   Mensagem exibida: '{error_message_element.text}'")
            print(f"   Mensagem esperada: '{EXPECTED_ERROR_MESSAGE}'")
        else:
            print("\n❌ Teste FALHOU: O campo de senha está vazio, mas a mensagem de erro não foi exibida.")
            
    except NoSuchElementException:
        print("\n❌ Teste FALHOU: Um ou mais elementos necessários (campos ou botão 'Entrar') ou a mensagem de erro não foram encontrados na página.")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro inesperado durante o teste: {e}")

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_empty_password(driver)
        finally:
            print("\nTeste concluído. Fechando o navegador em 5 segundos...")
            time.sleep(5)
            driver.quit()