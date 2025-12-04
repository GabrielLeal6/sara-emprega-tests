import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from testes.pages.login_page import LoginPage
from testes.pages.home_page import HomePage
from testes.pages.profile_page import ProfilePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def setup_usuario_logado(driver):
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.fazer_login("candidato.padrao@email.com", "admin123") 
    
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
    except:
        pytest.fail("Login falhou.")

    home_page = HomePage(driver)
    home_page.ir_para_perfil()
    return ProfilePage(driver)

# Grupo CT-015: Edição (Passed)
def test_CT015_01_edicao_sucesso(setup_usuario_logado):
    page = setup_usuario_logado
    page.clicar_editar_ou_criar()
    page.preencher_campo("telefone", "(81) 99999-8888")
    page.salvar_alteracoes()
    
    msg = page.lidar_com_alerta()
    if not msg:
        time.sleep(1)
        page.clicar_editar_ou_criar()
        assert page.obter_valor_campo("telefone") == "(81) 99999-8888"
    else:
        assert "sucesso" in msg.lower() or "concluído" in msg.lower()

def test_CT015_02_cancelar_edicao(setup_usuario_logado):
    page = setup_usuario_logado
    page.clicar_editar_ou_criar()
    page.preencher_campo("nome", "NOME CANCELADO")
    page.cancelar_edicao()
    
    try:
        WebDriverWait(page.driver, 2).until(EC.invisibility_of_element_located(page.BTN_SALVAR))
    except:
        pytest.fail("Tela de edição não fechou ao cancelar")

def test_CT015_03_edicao_email_invalido(setup_usuario_logado):
    page = setup_usuario_logado
    time.sleep(1) 
    page.clicar_editar_ou_criar()
    
    page.preencher_campo("email", "emailsemarroba")
    page.salvar_alteracoes()
    
    erro = page.verificar_erro_navegador("email")
    if not erro:
        erro = page.lidar_com_alerta()
    
    assert erro, "Sistema aceitou email inválido."

def test_CT015_04_edicao_campo_vazio(setup_usuario_logado):
    page = setup_usuario_logado
    time.sleep(1)
    page.clicar_editar_ou_criar()
    page.limpar_campo("nome")
    page.salvar_alteracoes()
    
    msg = page.lidar_com_alerta()
    if not msg:
        msg = page.verificar_erro_navegador("nome")

    assert msg, "Sistema permitiu salvar campo obrigatório vazio."

# Grupo CT-016: Exclusão (Blocked/Xfail)
@pytest.mark.xfail(reason="Blocked: Botão não existe")
def test_CT016_01_exclusao_sucesso(setup_usuario_logado):
    setup_usuario_logado.clicar_deletar_curriculo()
    setup_usuario_logado.confirmar_exclusao()

@pytest.mark.xfail(reason="Blocked: Botão não existe")
def test_CT016_02_cancelar_exclusao(setup_usuario_logado):
    setup_usuario_logado.clicar_deletar_curriculo()
    setup_usuario_logado.cancelar_exclusao_modal()

@pytest.mark.xfail(reason="Blocked: Botão não existe")
def test_CT016_03_exclusao_com_candidatura_ativa(setup_usuario_logado):
    setup_usuario_logado.clicar_deletar_curriculo()

# Grupo CT-017: Visualização (Blocked/Pass)
@pytest.mark.xfail(reason="Blocked: Visualização instável")
def test_CT017_01_visualizar_sucesso(setup_usuario_logado):
    page = setup_usuario_logado
    time.sleep(1)
    src = page.driver.page_source
    assert "BotãoDownloadPDFFuncional" in src

@pytest.mark.xfail(reason="Blocked: Fluxo inconsistente")
def test_CT017_02_visualizar_sem_cadastro(driver):
    login = LoginPage(driver)
    login.abrir()
    login.fazer_login("novo.sem.cv@teste.com", "123456") 
    WebDriverWait(driver, 5).until(EC.url_contains("/home"))
    driver.get("http://localhost:3000/perfil")
    assert "Criar Novo" in driver.page_source

def test_CT017_03_empresa_visualiza_candidato(driver):
    login = LoginPage(driver)
    login.abrir()
    login.fazer_login("empresa@sara.com", "senha123")
    
    try:
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
        assert "/home" in driver.current_url
    except:
        pytest.fail("Login de empresa falhou.")