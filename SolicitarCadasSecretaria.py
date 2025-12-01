"""teste ct005.02 Solicitar cadastro com campo vazio"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import random

CHROME_DRIVER_PATH = '/path/to/chromedriver'
CADASTRO_URL = 'http://localhost:3000/cadastro/secretaria'
LOGIN_URL = 'http://localhost:3000/login' 

# Dados válidos para preencher os outros campos
SEMESTER = str(random.randint(1, 99999)) 
DUMMY_DATA = {
    "Endereco": "Rua Teste de Validação, 100",
    "Telefone": "81990000000",
    "Email": f"teste.vazio.{SEMESTER}@secretaria.gov",
    "Senha": "Senha1234",
}
EXPECTED_ERROR_MESSAGE = 'Campo obrigatório' 

def setup_driver():
    """Inicializa o WebDriver."""
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

def test_empty_name_field(driver):
    
    print(f"1.  Acessando a tela de Cadastro de Secretaria: {CADASTRO_URL}")
    driver.get(CADASTRO_URL)
    time.sleep(2) 
    
    try:
        # 1. Localizar o campo Nome e DEIXAR VAZIO
        name_field = driver.find_element(By.XPATH, "//input[@placeholder='Nome da secretaria']")
        print("2.  Deixando o campo Nome em branco.")

        print("3. Preenchendo os demais campos...")
        
        # Endereço (Segundo input de texto)
        driver.find_element(By.XPATH, "//input[@placeholder='Endereço completo']").send_keys(DUMMY_DATA["Endereco"])

        # Telefone
        driver.find_element(By.XPATH, "//input[@placeholder='(00) 00000-0000']").send_keys(DUMMY_DATA["Telefone"])
        
        # Email
        driver.find_element(By.XPATH, "//input[@placeholder='contato@secretaria.gov']").send_keys(DUMMY_DATA["Email"])
        
        # Senha
        driver.find_element(By.XPATH, "//input[@placeholder='Crie uma senha']").send_keys(DUMMY_DATA["Senha"])
        
        # Confirmar Senha
        driver.find_element(By.XPATH, "//input[@placeholder='Confirme a senha']").send_keys(DUMMY_DATA["Senha"])
        
        # 3. Tentar clicar no botão "Cadastrar" (ou "Solicitar cadastro" se o texto for esse)
        cadastro_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Cadastrar')]")
        print('4. 🖱️ Clicando em "Cadastrar"...')
        cadastro_button.click()
        time.sleep(2) 

        # 4. Verificação
        
        # Verifica se o sistema exibiu uma mensagem de erro ou se permaneceu na mesma URL.
        current_url = driver.current_url
        
        try:
            # Tenta encontrar uma mensagem de erro de validação (Se a validação for do lado do servidor ou JS)
            error_message = driver.find_element(By.XPATH, f"//*[contains(text(), '{EXPECTED_ERROR_MESSAGE}')]")
            if error_message.is_displayed() or current_url == CADASTRO_URL:
                print("\n Teste PASSOU: O cadastro foi impedido/erro de validação exibido.")
            else:
                print("\n Teste FALHOU: A página avançou/redirecionou, indicando que o campo vazio foi aceito.")
        except NoSuchElementException:
            if current_url == CADASTRO_URL:
                 print("\n Teste PASSOU: A página permaneceu na tela de cadastro. O envio foi bloqueado.")
            else:
                 print(f"\n Teste FALHOU: O sistema permitiu o envio. Redirecionado para: {current_url}")

    except NoSuchElementException:
        print("\n Teste FALHOU: Elementos do formulário não foram encontrados.")
    except Exception as e:
        print(f"\n Ocorreu um erro: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_empty_name_field(driver)
        finally:
            time.sleep(5)
            driver.quit()