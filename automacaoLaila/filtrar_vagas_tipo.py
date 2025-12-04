# Comando para rodar: pytest automacaoLaila/filtrar_vagas_tipo.py
'''
Esse caso de teste corresponde à 
filtragem de vagas por tipo de contrato
'''
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

# Configurações
LOGIN_URL = "https://sara-frontend-736daffd516a.herokuapp.com/login"
HOME_EMPRESA_URL_FRAGMENT = "/home/empresa"
VAGAS_PUBLICAS_URL = "https://sara-frontend-736daffd516a.herokuapp.com/vagas" # URL pública para o teste de filtro
VAGAS_PUBLICAS_FRAGMENT = "/vagas" 
DEFAULT_TIMEOUT = 30 


def test_filtrar_vaga_por_clt(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    REGIME_FILTRO = "CLT"

    print(f"\n--- INICIANDO TESTE: Filtragem por Regime de Contratação ({REGIME_FILTRO}) ---")

    # 1) Abrir a tela de login
    driver.get(LOGIN_URL)
    print(f"1. Acessada URL: {LOGIN_URL}")
    time.sleep(5) 

    # 2) Preencher credenciais 
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("empresa@sara.com")
    
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("senha123")
    print("2. Credenciais preenchidas.")

    # 3) Clicar Entrar
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Entrar']"))).click()
    print("3. Clicado em 'Entrar'. Aguardando login ser processado.")

    # 4) Aguardar redirecionamento para a tela inicial da empresa (Formulário)
    wait.until(EC.url_contains(HOME_EMPRESA_URL_FRAGMENT))
    print(f"4. Redirecionamento inicial para {HOME_EMPRESA_URL_FRAGMENT} confirmado (Autenticação concluída).")
    
    # 5) Navegar diretamente para a lista de vagas PÚBLICAS (/vagas)
    print(f"5. Redirecionando diretamente para a URL de vagas PÚBLICAS: {VAGAS_PUBLICAS_URL}")
    driver.get(VAGAS_PUBLICAS_URL)
    
    # 6) Confirma que a URL está correta e aguarda o carregamento da página.
    wait.until(EC.url_contains(VAGAS_PUBLICAS_FRAGMENT))
    print(f"6. Confirmação: A URL atual é {VAGAS_PUBLICAS_FRAGMENT}.")
    time.sleep(2) # Pausa para garantir que a lista e os ícones de filtro carreguem

    # 7) Clicar no ícone de filtro para abrir o modal de filtros
    print("7. Buscando e clicando no ícone de filtro (Funil) para abrir as opções...")
    
    filtro_btn_xpath = "//button[./*[name()='svg' and contains(@class, 'lucide-funnel')]]" 
    
    try:
        filtro_btn = wait.until(EC.element_to_be_clickable((By.XPATH, filtro_btn_xpath)))
        filtro_btn.click()
        print("7.1. Ícone de filtro clicado com sucesso.")
    except TimeoutException:
         raise AssertionError("Falha: O botão de filtro (ícone de filtro) não foi encontrado ou não está clicável.")

    time.sleep(1) # Aguarda o modal de filtro abrir

    # 8) Marcar a opção 'CLT'
    input_clt_xpath = f"//input[@type='checkbox' and @id='{REGIME_FILTRO}']"
    
    print(f"8. Buscando e clicando no checkbox para: '{REGIME_FILTRO}'...")
    try:
        input_clt = wait.until(EC.element_to_be_clickable((By.XPATH, input_clt_xpath)))
        input_clt.click()
        print(f"8.1. Checkbox '{REGIME_FILTRO}' marcada com sucesso.")
    except TimeoutException:
        raise AssertionError(f"Falha: O checkbox com ID='{REGIME_FILTRO}' não foi encontrado ou não está clicável.")
    
    time.sleep(1) # Aguarda a aplicação do filtro

    # 9) Validar resultado: a tag de regime 'CLT' deve aparecer
    # O XPath busca o span com o texto "CLT" (span[normalize-space()='CLT'])
    tag_resultado_xpath = f"//span[normalize-space()='{REGIME_FILTRO}']"

    print(f"9. Aguardando a vaga filtrada com o regime '{REGIME_FILTRO}' aparecer...")
    
    try:
        # Timeout para carregar o resultado da filtragem
        wait_long = WebDriverWait(driver, 60) 
        resultado_tag = wait_long.until(EC.visibility_of_element_located((By.XPATH, tag_resultado_xpath)))
        print(f"   SUCESSO: Encontrado o regime '{resultado_tag.text}' no resultado da vaga.")
    except TimeoutException:
        raise AssertionError(f"Falha: Nenhuma vaga com o regime '{REGIME_FILTRO}' apareceu após a filtragem. Timeout de 60s.")

    time.sleep(2)
    
    print("--- TESTE DE FILTRAGEM POR REGIME FINALIZADO COM SUCESSO ---")