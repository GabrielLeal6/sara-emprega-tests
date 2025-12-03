import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options # Importação Adicionada
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def setup_browser():
    # 1. Configura as opções do Chrome para desabilitar o gerenciador de senhas e popups
    chrome_options = Options()
    
    # Este dicionário de preferências desabilita os popups nativos do Google Chrome
    # relacionados a senhas e sugestões de salvamento/alteração.
    prefs = {
        "credentials_enable_service": False, 
        "profile.password_manager_enabled": False 
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Adiciona argumentos para desabilitar popups de notificação e de salvar senha, 
    # fornecendo uma camada extra de proteção contra interrupções.
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-notifications") # Boa prática geral

    # 2. Configura o ChromeDriver automaticamente
    service = ChromeService(ChromeDriverManager().install())
    
    # 3. Inicializa o WebDriver, PASSANDO as opções configuradas
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Configurações iniciais
    driver.implicitly_wait(10) # Tempo de espera implícito em segundos
    driver.maximize_window()
    
    # O 'yield' retorna o objeto driver para os testes. 
    # Tudo abaixo dele é o 'teardown' (executado ao final)
    yield driver
    
    # 4. Teardown: Fechar o browser após a conclusão de todos os testes
    print("\nFechando o navegador...")
    driver.quit()