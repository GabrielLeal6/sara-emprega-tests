# conftest.py

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def setup_browser():
    # 1. Configura o ChromeDriver automaticamente
    # Isso baixa e gerencia a versão correta do Chrome Driver
    service = ChromeService(ChromeDriverManager().install())
    
    # 2. Inicializa o WebDriver
    driver = webdriver.Chrome(service=service)
    
    # Configurações iniciais
    driver.implicitly_wait(10) # Tempo de espera implícito em segundos
    driver.maximize_window()
    
    # O 'yield' retorna o objeto driver para os testes. 
    # Tudo abaixo dele é o 'teardown' (executado ao final)
    yield driver
    
    # 3. Teardown: Fechar o browser após a conclusão de todos os testes
    print("\nFechando o navegador...")
    driver.quit()