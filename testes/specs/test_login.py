import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from testes.pages.login_page import LoginPage
import time

@pytest.fixture
def login_page():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    page = LoginPage(driver)
    page.abrir()
    yield page
    driver.quit()

# CT-001.01: Login com credenciais válidas
def test_login_sucesso(login_page):
    login_page.fazer_login("candidato.padrao@email.com", "admin123") 
    assert login_page.esta_na_home() == True, "Erro: Não redirecionou para a Home."

# CT-001.02: Login com senha inválida
def test_login_senha_invalida(login_page):
    login_page.fazer_login("teste@mail.com", "SenhaErrada")
    msg = login_page.obter_mensagem_erro_global()
    # Verifica parte da string pois a mensagem completa pode variar
    assert "Credenciais inválidas" in msg

# CT-001.03: Login com e-mail inexistente
def test_login_email_inexistente(login_page):
    login_page.fazer_login("naoexiste@mail.com", "QualquerSenha")
    msg = login_page.obter_mensagem_erro_global()
    assert "Credenciais inválidas" in msg

# CT-001.04: Tentativa de login com conta inativa
def test_login_conta_inativa(login_page):

    login_page.fazer_login("usuarioinativo@mail.com", "SenhaValida123")

    msg = login_page.obter_mensagem_erro_global()

    assert "Credenciais inválidas" in msg or "conta pendente" in msg or "conta inativa" in msg  # sujeito a mudança no texto aqui

# CT-001.05: Login com campos vazios
def test_login_campos_vazios(login_page):
    login_page.fazer_login("", "")
    
    msg_email = login_page.obter_erro_campo_email()
    assert msg_email == "O campo de e-mail é obrigatório."
    
    msg_senha = login_page.obter_erro_campo_senha()
    assert msg_senha == "O campo de senha é obrigatório."