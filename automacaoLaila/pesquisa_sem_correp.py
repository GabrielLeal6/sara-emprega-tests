# Comando para rodar: pytest automacaoLaila/pesquisa_sem_correp.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys # Importação necessária para simular o ENTER

# Configurações
LOGIN_URL = "https://sara-frontend-736daffd516a.herokuapp.com/login"
HOME_EMPRESA_URL_FRAGMENT = "/home/empresa"
VAGAS_PUBLICAS_URL = "https://sara-frontend-736daffd516a.herokuapp.com/vagas" # URL pública para o teste de pesquisa
VAGAS_PUBLICAS_FRAGMENT = "/vagas" # Fragmento para validação robusta
DEFAULT_TIMEOUT = 30 

# Função auxiliar para simular a digitação lenta
def slow_send_keys(element, text, delay=0.2):
    """Digita o texto no elemento, caractere por caractere, com um atraso entre eles."""
    for character in text:
        element.send_keys(character)
        time.sleep(delay)

def test_pesquisar_vaga_sem_resultado(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # Termo de busca que não deve retornar nenhuma vaga
    TERMO_BUSCA = "fregrger"
    # Mensagem esperada quando não há resultados
    MENSAGEM_NAO_ENCONTRADA = "Nenhuma vaga encontrada com os filtros atuais."

    print(f"\n--- INICIANDO TESTE: Pesquisa de Vaga sem Resultado (Termo: {TERMO_BUSCA}) ---")

    # 1) Abrir a tela de login
    driver.get(LOGIN_URL)
    print(f"1. Acessada URL: {LOGIN_URL}")
    
    # Pausa crítica para estabilizar o carregamento inicial da URL
    time.sleep(5) 

    # 2) Preencher credenciais (com .clear() para garantir a estabilidade)
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("empresa@sara.com")
    
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("senha123")
    print("2. Credenciais preenchidas.")

    # 3) Clicar Entrar
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Entrar']"))).click()
    print("3. Clicado em 'Entrar'. Aguardando login ser processado.")

    # 4) Aguardar redirecionamento para a tela inicial da empresa
    wait.until(EC.url_contains(HOME_EMPRESA_URL_FRAGMENT))
    print(f"4. Redirecionamento inicial para {HOME_EMPRESA_URL_FRAGMENT} confirmado (Autenticação concluída).")
    
    # 5) Navegar diretamente para a lista de vagas PÚBLICAS (/vagas)
    print(f"5. Redirecionando diretamente para a URL de vagas PÚBLICAS: {VAGAS_PUBLICAS_URL}")
    driver.get(VAGAS_PUBLICAS_URL)
    
    # 6) Confirma que a URL está correta e aguarda o carregamento da página de pesquisa.
    wait.until(EC.url_contains(VAGAS_PUBLICAS_FRAGMENT))
    print(f"6. Confirmação: A URL atual é {VAGAS_PUBLICAS_FRAGMENT}.")
    
    # 7) Pesquisar pelo termo inexistente
    print(f"7. Buscando pelo termo: '{TERMO_BUSCA}'...")
    
    # Localizador do campo de busca pelo placeholder
    search_input_xpath = "//input[@placeholder='Pesquisar por cargo, empresa...']"
    
    # O elemento deve estar visível na URL de listagem pública
    search_input = wait.until(EC.visibility_of_element_located((By.XPATH, search_input_xpath)))
    
    # Limpa o campo (e aguarda para visualização)
    search_input.clear()
    time.sleep(1) 
    print("7.1. Campo de busca limpo.")

    # Digita o termo lentamente
    slow_send_keys(search_input, TERMO_BUSCA, 0.2)
    time.sleep(1) 
    print(f"7.2. Termo digitado: '{TERMO_BUSCA}' lentamente.")
    
    # Pressionar ENTER
    search_input.send_keys(Keys.ENTER)
    time.sleep(1) 
    print("7.3. ENTER pressionado. Aguardando a mensagem de resultado vazio...")

    # 8) Checar a mensagem de "Nenhuma vaga encontrada"
    # O XPath busca o div com o texto exato da mensagem de resultado vazio
    resultado_vazio_xpath = f"//div[normalize-space()='{MENSAGEM_NAO_ENCONTRADA}']"
    
    print(f"8. Aguardando aparecer a mensagem: '{MENSAGEM_NAO_ENCONTRADA}'...")
    
    try:
        # Aumentei o timeout para dar tempo da pesquisa carregar
        wait_long = WebDriverWait(driver, 60) 
        resultado_vazio = wait_long.until(EC.visibility_of_element_located((By.XPATH, resultado_vazio_xpath)))
        print(f"   SUCESSO: Encontrada a mensagem de resultado vazio: '{resultado_vazio.text}'.")
    except TimeoutException:
        raise AssertionError(f"Falha: A mensagem de resultado vazio ('{MENSAGEM_NAO_ENCONTRADA}') não apareceu. Alguma vaga inesperada foi encontrada. Timeout de 60s.")

    time.sleep(2)
    
    print("--- TESTE DE PESQUISA SEM RESULTADO FINALIZADO COM SUCESSO ---")
