"""teste ct001.02: fazer login com senha vazia"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/login' 

VALID_EMAIL = 'fulanoadmnato@sara.com'
INVALID_PASSWORD = 'semsenha'

EXPECTED_ERROR_MESSAGE = 'Credenciais inválidas' 

def setup_driver():
    try:
        if CHROME_DRIVER_PATH and CHROME_DRIVER_PATH != '/path/to/chromedriver':
             service = Service(CHROME_DRIVER_PATH)
             driver = webdriver.Chrome(service=service)
        else:
            driver = webdriver.Chrome()
        return driver
    except WebDriverException:
        return None

def test_invalid_password(driver):
    initial_url = LOGIN_URL
    driver.get(initial_url)
    time.sleep(2) 
    
    try:
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')
        email_field.send_keys(VALID_EMAIL)
        
        """password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password_field.send_keys(INVALID_PASSWORD)"""
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()

        time.sleep(3) 
        
        current_url = driver.current_url
        
        # Tentativa de verificar uma mensagem de erro, se existir
        try:
            error_message_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{EXPECTED_ERROR_MESSAGE}')]")
            if error_message_element.is_displayed():
                 print("Teste PASSOU: A mensagem de erro esperada foi exibida.")
            else:
                print("Teste FALHOU: O erro não foi exibido.")
        except NoSuchElementException:
            # Se não houver uma mensagem específica, verifica se permaneceu na URL de login
            if current_url == initial_url:
                print("Teste PASSOU: Permaneceu na página de login. Login inválido detectado.")
            else:
                print(f"Teste FALHOU: Redirecionado para {current_url}. O login falhou inesperadamente.")
            
    except NoSuchElementException:
        print("Teste FALHOU: Elementos não encontrados.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_invalid_password(driver)
        finally:
            time.sleep(5)
            driver.quit()