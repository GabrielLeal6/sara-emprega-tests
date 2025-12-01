import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Importamos a classe que criamos no passo anterior
# Nota: o ponto antes de pages (.pages) indica que está na pasta vizinha
import sys
import os

# Ajuste técnico para o Python achar a pasta 'pages'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    # Isso abre o navegador Chrome automaticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    # Isso fecha o navegador quando o teste acaba
    driver.quit()

def test_interacao_login(driver):
    """
    Objetivo: Verificar se conseguimos digitar nos campos de login.
    Não testamos o login real (back-end), apenas a interface.
    """
    
    # 1. Inicia a página
    pagina = LoginPage(driver)
    pagina.abrir()

    # 2. Define dados de teste
    email_teste = "teste@exemplo.com"
    senha_teste = "123456"

    # 3. O Robô interage
    pagina.preencher_email(email_teste)
    pagina.preencher_senha(senha_teste)
    
    # (Opcional) Clica no botão só para ver se não quebra
    # pagina.clicar_entrar() 

    # 4. VALIDAÇÃO (O momento da verdade)
    # Perguntamos ao navegador: "O que está escrito no campo email agora?"
    valor_atual = pagina.obter_valor_email()

    # Se o que digitamos for igual ao que está lá, o teste PASSOU!
    assert valor_atual == email_teste