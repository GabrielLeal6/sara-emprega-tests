"""
Teste de pesquisa de vaga pelo título.
Executar com: pytest automacaoLaila/pesquisar_vaga.py
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys 

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

def test_pesquisar_vaga_por_titulo(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    print("\n--- INICIANDO TESTE: Pesquisa de Vaga por Título (Navegação Direta) ---")

    # 1) Abrir a tela de login
    driver.get(LOGIN_URL)
    print(f"1. Acessada URL: {LOGIN_URL}")
    
    # Pausa crítica para estabilizar o carregamento inicial da URL e evitar o erro 'data:,'
    time.sleep(5) 

    # 2) Preencher credenciais (com .clear() para garantir a estabilidade)
    # A espera (wait.until) garante que o elemento foi carregado no DOM.
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("empresa@sara.com")
    
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("senha123")
    print("2. Credenciais preenchidas.")

    # 3) Clicar Entrar
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Entrar']"))).click()
    print("3. Clicado em 'Entrar'. Aguardando login ser processado.")

    # 4) Aguardar redirecionamento para a tela inicial da empresa (Formulário)
    # Isso garante que a autenticação foi concluída antes de forçar a navegação.
    wait.until(EC.url_contains(HOME_EMPRESA_URL_FRAGMENT))
    print(f"4. Redirecionamento inicial para {HOME_EMPRESA_URL_FRAGMENT} confirmado (Autenticação concluída).")
    
    # 5) Navegar diretamente para a lista de vagas PÚBLICAS (/vagas)
    # Ignora o formulário de vagas sem interagir com ele.
    print(f"5. Redirecionando diretamente para a URL de vagas PÚBLICAS: {VAGAS_PUBLICAS_URL}")
    driver.get(VAGAS_PUBLICAS_URL)
    
    # 6) Confirma que a URL está correta e aguarda o carregamento da página de pesquisa.
    wait.until(EC.url_contains(VAGAS_PUBLICAS_FRAGMENT))
    print(f"6. Confirmação: A URL atual é {VAGAS_PUBLICAS_FRAGMENT}.")
    
    # 7) Pesquisar pela vaga
    TERMO_BUSCA = "Desenvolvedor"
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
    print(f"7.2. Termo digitado: '{TERMO_BUSCA}'.")
    
    # Pressionar ENTER
    search_input.send_keys(Keys.ENTER)
    time.sleep(1) 
    print("7.3. ENTER pressionado. Aguardando resultados...")

    # 8) Checar o resultado
    RESULTADO_ESPERADO_FRAGMENTO = TERMO_BUSCA
    # O XPath busca por um elemento de texto com 'Desenvolvedor' e a classe 'text-black' (presumindo ser o título)
    resultado_xpath = f"//*[contains(text(), '{RESULTADO_ESPERADO_FRAGMENTO}') and contains(@class, 'text-black')]"
    
    print(f"8. Aguardando aparecer na tela um resultado com o texto: '{RESULTADO_ESPERADO_FRAGMENTO}'...")
    
    try:
        # Timeout para dar tempo da pesquisa carregar
        wait_long = WebDriverWait(driver, 60) 
        resultado_vaga = wait_long.until(EC.visibility_of_element_located((By.XPATH, resultado_xpath)))
        print(f"   SUCESSO: Encontrado o título da vaga: '{resultado_vaga.text}' na lista de resultados.")
    except TimeoutException:
        raise AssertionError(f"Falha: Nenhum resultado de vaga contendo '{RESULTADO_ESPERADO_FRAGMENTO}' apareceu após a pesquisa. Timeout de 60s.")

    time.sleep(2)
    
    print("--- TESTE DE PESQUISA POR TÍTULO FINALIZADO COM SUCESSO ---")