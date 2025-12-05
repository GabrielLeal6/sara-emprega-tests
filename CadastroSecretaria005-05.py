"""teste ct005.05: Solicitar cadastro com email no formato errado"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import random

CHROME_DRIVER_PATH = '/path/to/chromedriver'
CADASTRO_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/cadastro/secretaria'

# Dados para preencher os campos. O e-mail será o valor inválido.
INVALID_EMAIL = 'fernanda@@semas' 
SEMESTER = str(random.randint(1, 99999)) 
DUMMY_DATA = {
    "Nome": f"Secretaria Teste {SEMESTER}",
    "Endereco": "Rua Teste de Email, 200",
    "Telefone": "81991111111",
    "Senha": "Senha4321#",
}
EXPECTED_ERROR_MESSAGE = 'E-mail inválido' 

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

def test_invalid_email_format(driver):
    
    print(f"1.  Acessando a tela de Cadastro de Secretaria: {CADASTRO_URL}")
    driver.get(CADASTRO_URL)
    time.sleep(2) 
    
    try:
        # 2. Preencher os campos restantes
        print("2.  Preenchendo todos os campos, incluindo o e-mail inválido...")
        
        # Nome
        driver.find_element(By.XPATH, "//input[@placeholder='Nome da secretaria']").send_keys(DUMMY_DATA["Nome"])

        # Endereço
        driver.find_element(By.XPATH, "//input[@placeholder='Endereço completo']").send_keys(DUMMY_DATA["Endereco"])

        # Telefone
        driver.find_element(By.XPATH, "//input[@placeholder='(00) 00000-0000']").send_keys(DUMMY_DATA["Telefone"])
        
        # E-mail (Onde o erro será injetado)
        email_field = driver.find_element(By.XPATH, "//input[@placeholder='contato@secretaria.gov']")
        email_field.send_keys(INVALID_EMAIL)
        
        # Senha
        driver.find_element(By.XPATH, "//input[@placeholder='Crie uma senha']").send_keys(DUMMY_DATA["Senha"])
        
        # Confirmar Senha
        driver.find_element(By.XPATH, "//input[@placeholder='Confirme a senha']").send_keys(DUMMY_DATA["Senha"])
        
        # 3. clicar no botão "Cadastrar"
        cadastro_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Cadastrar')]")
        print('3.  Clicando em "Cadastrar"...')
        cadastro_button.click()
        time.sleep(2) 

        # 4. Verificação
        current_url = driver.current_url
        
        try:
            error_message = driver.find_element(By.XPATH, f"//*[contains(text(), '{EXPECTED_ERROR_MESSAGE}')]")
            if error_message.is_displayed() or current_url == CADASTRO_URL:
                print("\n Teste PASSOU: O cadastro foi impedido/erro de validação exibido.")
            else:
                print("\n Teste FALHOU: A página avançou/redirecionou, indicando que o formato inválido foi aceito.")
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
            test_invalid_email_format(driver)
        finally:
            time.sleep(5)
            driver.quit()