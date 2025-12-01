"""teste ct001.01: fazer login com sucesso"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'http://localhost:3000/login'

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
        return None

def test_valid_login(driver):
    initial_url = LOGIN_URL
    driver.get(initial_url)
    time.sleep(2)
    
    try:
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')
        email_field.send_keys(VALID_EMAIL)
        
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        password_field.send_keys(VALID_PASSWORD)
        
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        login_button.click()

        time.sleep(5) 
        
        current_url = driver.current_url
        
        if current_url != initial_url:
            print(f"Teste PASSOU: O login foi bem-sucedido e o driver foi redirecionado para: {current_url}")
        else:
            print("Teste FALHOU: Permaneceu na página de login. O login pode ter falhado.")

    except NoSuchElementException:
        print("Teste FALHOU: Elementos de E-mail, Senha ou botão 'Entrar' não foram encontrados.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_valid_login(driver)
        finally:
            time.sleep(5)
            driver.quit()