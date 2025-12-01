"""teste ct015.01: editar curriculo"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CHROME_DRIVER_PATH = '/path/to/chromedriver'
PROFILE_URL = 'http://localhost:3000/perfil' 
NOVO_TELEFONE = '(81) 91111-2222'

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

def test_edit_curriculum_success(driver):
    driver.get(PROFILE_URL)
    time.sleep(2) 

    try:
        # 1. Clicar em "Editar Currículo"
        # Usando WebDriverWait para garantir que o botão "Editar Currículo" esteja carregado
        edit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Editar Currículo')]"))
        )
        edit_button.click()
        print("1. Clicou em 'Editar Currículo'.")
        time.sleep(2) 

        # --- Rolagem para garantir que o campo e o botão "Salvar" estejam visíveis ---
        print("2. Rolando a tela para garantir que todos os campos estejam visíveis...")
        
        # Localiza o botão "Salvar alterações" 
        save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Salvar alterações')]")
        
        # O comando JavaScript rola até o elemento e o coloca no centro da tela
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
        time.sleep(1) 

        # 3. Localizar e alterar campo "Número"
        print(f"3. Alterando campo 'Número' para {NOVO_TELEFONE}...")
        
        # Tentativa de localizar o campo de input de número pelo placeholder ou um label associado ao texto "Número"
        try:
             
             numero_field = driver.find_element(By.XPATH, "//div[contains(text(), 'Número')]/following-sibling::input")
        except NoSuchElementException:
             # encontrar o campo com o valor anterior do telefone (81) 98888-7777 (visto no seu screenshot)
             numero_field = driver.find_element(By.XPATH, "//input[@value='(81) 98888-7777']")
             
        numero_field.clear()
        numero_field.send_keys(NOVO_TELEFONE)
        time.sleep(1)

        # 4. Clicar em "Salvar alterações" 
        print("4. Clicando em 'Salvar alterações'...")
        save_button.click()
        time.sleep(3) 

        # 5. Verificação: Tenta verificar se o novo número está presente na página
        updated_number = driver.find_element(By.XPATH, f"//*[contains(text(), '{NOVO_TELEFONE}')]")
        
        if updated_number.is_displayed():
            print(f" Teste PASSOU: O campo Número foi atualizado com sucesso para {NOVO_TELEFONE}.")
        else:
            print(" Teste FALHOU: O novo número não foi encontrado na tela após salvar.")

    except (NoSuchElementException, TimeoutException):
        print(" Teste FALHOU: Elementos importantes ('Editar Currículo', campo Número, ou 'Salvar alterações') não foram encontrados mesmo após a rolagem.")
    except Exception as e:
        print(f" Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_edit_curriculum_success(driver)
        finally:
            time.sleep(5)
            driver.quit()