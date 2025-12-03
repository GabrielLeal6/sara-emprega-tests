import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from testes.pages.login_page import LoginPage
from testes.pages.home_page import HomePage

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

@pytest.fixture
def usuario_logado(driver):
    login_page = LoginPage(driver)
    home_page = HomePage(driver)
    
    login_page.abrir()
    login_page.fazer_login("candidato.padrao@email.com", "admin123")
    
    assert login_page.esta_na_home(), "Setup falhou: login não realizado"
    
    return login_page, home_page

# CT-002.01: Logout com sucesso
def test_logout_sucesso(usuario_logado):
    login_page, home_page = usuario_logado
    
    home_page.fazer_logout()
    assert login_page.esta_na_pagina_login()

# CT-002.02: Bloqueio de acesso pós-logout
def test_acesso_restrito_pos_logout(usuario_logado):
    login_page, home_page = usuario_logado
    
    # 1. Sai do sistema
    home_page.fazer_logout()
    assert login_page.esta_na_pagina_login()
    
    # 2. Tenta voltar pela URL
    home_page.tentar_acessar_home_diretamente()
    
    # 3. Valida bloqueio (espera redirect primeiro para evitar race condition)
    assert login_page.esta_na_pagina_login()
    assert login_page.esta_na_home() == False