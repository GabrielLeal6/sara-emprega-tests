import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from testes.pages.login_page import LoginPage
from testes.pages.home_page_secretaria import UserRegistrationPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

@pytest.fixture
def setup_secretaria_logada(driver):
    login_page = LoginPage(driver)
    login_page.abrir()
    login_page.fazer_login("secretaria@daqui.com", "admin123") 
    WebDriverWait(driver, 10).until(EC.url_contains("/home/secretaria"))
    return UserRegistrationPage(driver)

VALID_DATA = {
    "email": "novo1.usuario@teste.com",
    "telefone": "(99) 99929-9999", 
    "endereco": "Rua 2este, 123, Centro",
    "password": "Se2ha@Valida123",
    "confirmpassword": "Se2ha@Valida123",
}

# Test CT-009.06: Cadastro com dado excedendo o limite de caracteres.
def test_cadastro_nome_excede_limite(setup_secretaria_logada):
    page = setup_secretaria_logada
    nome_longo = "A" * 51 
    page.preencher_e_enviar(
        name=nome_longo,
        email=VALID_DATA["email"],
        telefone=VALID_DATA["telefone"],
        endereco=VALID_DATA["endereco"],
        password=VALID_DATA["password"],
        confirmPassword=VALID_DATA["confirmpassword"]
    )
    msg_erro = page.obter_erro_campo("name")
    if msg_erro is None:
        msg_erro = page.obter_erro_cpf_invalido()
    assert msg_erro is not None, "Erro não apareceu"
    erro_limite = "no máximo 50 caracteres" in msg_erro
    erro_generico = "Ocorreu um erro" in msg_erro
    assert erro_limite or erro_generico

# CT-009.07: Cadastro com CPF inválido (mas no formato correto).
def test_cadastro_cpf_invalido(setup_secretaria_logada):
    page = setup_secretaria_logada
    page.preencher_e_enviar(
        name="Usuario com CPF Invalido", 
        email=VALID_DATA["email"],
        telefone=VALID_DATA["telefone"],
        endereco=VALID_DATA["endereco"],
        password=VALID_DATA["password"],
        confirmPassword=VALID_DATA["confirmpassword"]
    )
    msg_erro = page.obter_erro_cpf_invalido()
    assert msg_erro is not None, "Erro global não apareceu"
    erro_especifico = "CPF inválido" in msg_erro
    erro_generico = "Ocorreu um erro ao criar a conta" in msg_erro
    assert erro_especifico or erro_generico

# TESTE DE SUCESSO IMPLEMENTADO (esse não tem test case que na planilha ficou errado, 
# mas usei um suposto teste de para validar um sucesso no cadastro, depois eu arrumo isso na planilha)
def test_cadastro_sucesso(setup_secretaria_logada):
    page = setup_secretaria_logada
    
    # Gera um email único baseado no tempo para evitar erro de duplicidade
    email_dinamico = f"user_{int(time.time())}@teste.com"
    
    page.preencher_e_enviar(
        name="Usuario Valido Sucesso",
        email=email_dinamico,
        telefone=VALID_DATA["telefone"],
        endereco=VALID_DATA["endereco"],
        password=VALID_DATA["password"],
        confirmPassword=VALID_DATA["confirmpassword"]
    )
    
    # Verifica se o modal apareceu
    sucesso = page.verificar_sucesso()
    assert sucesso is True, "O modal de sucesso 'Cadastro Concluído!' não foi exibido na tela."