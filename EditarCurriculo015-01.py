from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# --- Configuração de URLs e Credenciais ---
CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/login'
HOME_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/home/user' 
PROFILE_URL = 'https://sara-frontend-736daffd516a.herokuapp.com/perfil'

VALID_EMAIL = 'candidato.padrao@email.com'
VALID_PASSWORD = 'admin123'
WAIT_TIME = 15 

# Dados de preenchimento de teste
TEST_ID = str(random.randint(100, 999))
CURRICULUM_DATA = {
    "Objetivo": f"Busco uma nova oportunidade desafiadora na área de QA e Automação de Testes. Mensagem de Teste {TEST_ID}"
}

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
        print("Erro ao configurar o WebDriver. Verifique o caminho do ChromeDriver.")
        return None

def test_full_curriculum_edit(driver):
    
    # --- ETAPA 1: Login ---
    print(f"1.  Acessando {LOGIN_URL} e fazendo login...")
    driver.get(LOGIN_URL)
    time.sleep(2) 
    
    try:
        # Preenche as credenciais e clica em Entrar
        email_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        
        email_field.send_keys(VALID_EMAIL)
        password_field.send_keys(VALID_PASSWORD)
        login_button.click()
        
        WebDriverWait(driver, WAIT_TIME).until(EC.url_to_be(HOME_URL))
        print("    Login bem-sucedido.")

        # --- ETAPA 2 & 3: Abrir Menu e Navegar para Perfil ---
        print("2 & 3.  Abrindo Menu e clicando em 'Perfil'...")
        
        menu_button = WebDriverWait(driver, WAIT_TIME).until(
             EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'menu')] | //header//button[1]"))
        )
        menu_button.click()
        time.sleep(2) 
        
        profile_link = WebDriverWait(driver, WAIT_TIME).until(
             EC.element_to_be_clickable((By.XPATH, "//a[text()='Perfil']"))
        )
        profile_link.click()
        
        WebDriverWait(driver, WAIT_TIME).until(EC.url_to_be(PROFILE_URL))
        print("    Navegação para Perfil bem-sucedida.")

        # --- ETAPA 4: Clicar em Atualizar / Criar Novo ---
        print("4.  Clicando em 'Atualizar / Criar Novo' para iniciar a edição...")
        update_button = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Atualizar / Criar Novo')]"))
        )
        update_button.click()
        # Garante que a nova página de edição carregue
        WebDriverWait(driver, WAIT_TIME).until(
             EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Salvar Currículo')]"))
        )
        time.sleep(3) 

        # --- ETAPA 5: Preencher APENAS Objetivo Profissional ---
        print("5.  Preenchendo APENAS o campo 'Objetivo Profissional'...")

        # Localiza o TextArea de forma estável
        objetivo_field = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Descreva seu objetivo profissional']"))
        )
        objetivo_field.clear()
        objetivo_field.send_keys(CURRICULUM_DATA["Objetivo"])
        
        # ----------------------------------------------------------------------------------

        # --- ETAPA 6: Rolar e Salvar ---
        print("6.  Rolando e clicando em 'Salvar Currículo'...")
        
        save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Salvar Currículo')]")
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
        time.sleep(5) 
        
        # Clica no botão
        save_button.click()
        
        # Verificação: Aguarda o pop-up de sucesso
        success_message = WebDriverWait(driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Currículo enviado e gerado com sucesso!')]"))
        )
        
        ok_button = driver.find_element(By.XPATH, "//button[text()='ok']")
        ok_button.click()
        
        print("\n Teste PASSOU: Objetivo Profissional preenchido e salvo com sucesso!")

    except TimeoutException:
         print(f"\n Teste FALHOU: Timeout. Um elemento (como o campo Objetivo Profissional ou o botão Salvar) não foi encontrado a tempo.")
    except Exception as e:
        print(f"\n Teste FALHOU: Erro inesperado: {e}")

if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_full_curriculum_edit(driver)
        finally:
            print("\nTeste concluído. Fechando o navegador em 5 segundos...")
            time.sleep(5)
            driver.quit()