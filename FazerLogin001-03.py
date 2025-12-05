"""TESTE CT001.03 Login com e-mail inexistente. """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time


# NOTE: 
CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/login' 


INVALID_EMAIL = 'email.nao.existe@mail.com'
VALID_PASSWORD = 'admin123'
EXPECTED_ERROR_MESSAGE = 'Credenciais inválidas'

def setup_driver():
    try:
        # Tenta inicializar o driver
        if CHROME_DRIVER_PATH and CHROME_DRIVER_PATH != '/path/to/chromedriver':
             service = Service(CHROME_DRIVER_PATH)
             driver = webdriver.Chrome(service=service)
        else:
            driver = webdriver.Chrome()
        
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure ChromeDriver is installed and its path is correctly configured.")
        return None

def test_login_invalid_email(driver):
   
    
    print(f"{LOGIN_URL}")
    driver.get(LOGIN_URL)
   
    time.sleep(2) 
    
    try:
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')

        email_field.send_keys(INVALID_EMAIL)
        
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        print(f" {'' * len(VALID_PASSWORD)}")
        password_field.send_keys(VALID_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()

        time.sleep(3)
        
        current_url = driver.current_url
        
        # Tenta encontrar a mensagem de erro no corpo da página
        try:
            error_message_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{EXPECTED_ERROR_MESSAGE}')]")
            if error_message_element.is_displayed() and current_url == LOGIN_URL:
                print("\n Teste PASSOU: Mensagem de erro exibida e permaneceu na página de login.")
            else:
                print("\n Teste FALHOU: Mensagem de erro não exibida ou houve redirecionamento.")
        except NoSuchElementException:
            if current_url == LOGIN_URL:
                 print("\n Teste PASSOU: Permaneceu na página de login (Falha implícita).")
            else:
                 print(f"\n Teste FALHOU: Redirecionado para: {current_url}. Login inesperadamente bem-sucedido.")

    except NoSuchElementException:
        print(" Teste FALHOU: Um ou mais elementos (Email/Password fields ou 'Entrar' button) não foram encontrados na página.")
    except Exception as e:
        print(f" An unexpected error occurred during the test: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_login_invalid_email(driver)
        finally:
            print("\n")
            time.sleep(5)
            driver.quit()