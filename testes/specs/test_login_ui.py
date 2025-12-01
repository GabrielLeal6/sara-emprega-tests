import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Adiciona o diretório pai ao sys.path e importa a página de login
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    # Isso abre o navegador Chrome automaticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    # fecha o navegador quando o teste acaba
    driver.quit()

def test_interacao_login(driver):
    """
    Objetivo: Verificar se conseguimos digitar nos campos de login.
    Não testamos o login real ainda (back-end), apenas a interface.
    """
    
    # Inicia a página
    pagina = LoginPage(driver)
    pagina.abrir()

    # dados de teste
    email_teste = "teste@exemplo.com"
    senha_teste = "123456"

    pagina.preencher_email(email_teste)
    pagina.preencher_senha(senha_teste)
    

    pagina.clicar_entrar() 

    # Validação do resultado
    valor_atual = pagina.obter_valor_email()

    # Se estiver igual passou
    assert valor_atual == email_teste