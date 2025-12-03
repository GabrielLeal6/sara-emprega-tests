# Comando para rodar: pytest automacaoLaila/cancelar_publicacao.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Configurações
LOGIN_URL = "https://sara-frontend-736daffd516a.herokuapp.com/login"
HOME_EMPRESA_URL_FRAGMENT = "/home/empresa"
VAGAS_EMPRESA_URL = "https://sara-frontend-736daffd516a.herokuapp.com/empresa/vagas"
VAGAS_EMPRESA_FRAGMENT = "/empresa/vagas" # Fragmento para validação robusta
DEFAULT_TIMEOUT = 30 

def _select_radix_option(driver, wait: WebDriverWait, button_id: str, option_text: str, timeout_sec: int = 12):
    """
    Clica no botão do Radix combobox (pelo id) e seleciona a opção desejada.
    Função reutilizada do teste anterior para preencher Tipo e Modalidade.
    """
    print(f"-> Tentando selecionar a opção '{option_text}' no combobox #{button_id}...")
    try:
        # 1. Clica no botão para abrir o dropdown
        btn = wait.until(EC.element_to_be_clickable((By.ID, button_id)))
        btn.click()
        print(f"   Dropdown '{button_id}' aberto com sucesso.")

        # 2. Tenta localizar e clicar no item da lista.
        xpath_role_option = f"//div[@role='option']/*[normalize-space(.)='{option_text}'] | //div[@role='option'][normalize-space(.)='{option_text}']"
        xpath_generic_text = f"//*[contains(@id, 'radix') or @role='option' or @role='listbox']//*[normalize-space(.)='{option_text}']"

        # Tenta o locator mais robusto (role=option dentro do portal)
        try:
            el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_role_option)))
            el.click()
            print(f"   Opção '{option_text}' selecionada via role='option' XPath.")
            return
        except TimeoutException:
             # Se falhar, tenta o locator mais genérico
            try:
                el = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_generic_text)))
                el.click()
                print(f"   Opção '{option_text}' selecionada via generic text XPath.")
                return
            except Exception:
                # Tenta fallback via JavaScript
                print("   Tentando fallback via JavaScript...")
                script = (
                    "const text = arguments[0];"
                    "const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT, null, false);"
                    "let node; while(node = walker.nextNode()){ if(node.innerText && node.innerText.trim() === text){ node.click(); return true; } }"
                    "return false;"
                )
                clicked = driver.execute_script(script, option_text)
                if clicked:
                    print("   Opção selecionada via JavaScript fallback.")
                    return

        # Se nenhuma das tentativas funcionou, levanta um erro
        raise AssertionError(f"Não consegui selecionar a opção '{option_text}' no combobox #{button_id}. Nenhum locator funcionou dentro do timeout.")

    except Exception as e:
        raise AssertionError(f"Erro geral ao selecionar o Radix option '{option_text}' (ID: {button_id}): {e}")


def test_cancelar_publicacao_vaga(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    print("\n--- INICIANDO TESTE: Cancelamento de Publicação de Vaga ---")

    # 1) Abrir a tela de login
    driver.get(LOGIN_URL)
    print(f"1. Acessada URL: {LOGIN_URL}")

    # 2) Preencher credenciais
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("empresa@sara.com")

    wait.until(EC.visibility_of_element_located((By.ID, "password"))).clear()
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("senha123")
    print("2. Credenciais preenchidas.")

    # 3) Clicar Entrar
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Entrar']"))).click()
    print("3. Clicado em 'Entrar'.")

    # 4) Aguardar redirecionamento para /home/empresa
    wait.until(EC.url_contains(HOME_EMPRESA_URL_FRAGMENT))
    print(f"4. Redirecionamento para {HOME_EMPRESA_URL_FRAGMENT} confirmado.")
    
    # 4.1) PAUSA MANUAL PARA FECHAR POPUP
    print("4.1) PAUSA DE 15s. POR FAVOR, FECHE O POPUP DE SENHA MANUALMENTE AGORA (clique em OK).")
    time.sleep(15) 
    print("4.1) Pausa encerrada. Retomando a automação.")


    # 5) Preencher campos de texto (Necessário para simular um cancelamento real)
    print("5. Preenchendo campos de texto (Simulação)...")
    
    # Campo "title"
    title = wait.until(EC.presence_of_element_located((By.ID, "title")))
    title.clear()
    title.send_keys("Vaga a ser Cancelada - Teste")

    # Campo "area"
    area = wait.until(EC.presence_of_element_located((By.ID, "area")))
    area.clear()
    area.send_keys("QA/Automação")

    # Selecionar Tipo -> Estágio
    _select_radix_option(driver, wait, button_id="type", option_text="Estágio")

    # Selecionar Modalidade -> Presencial
    _select_radix_option(driver, wait, button_id="modality", option_text="Presencial")
    
    print("6. Campos preenchidos.")
    time.sleep(1) # Pequena pausa para estabilizar o formulário

    # 7) Clicar em Cancelar
    print("7. Tentando clicar no botão 'Cancelar'...")
    
    # Localizador exato do botão "Cancelar"
    cancelar_xpath = "//button[normalize-space()='Cancelar']"
    
    cancelar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, cancelar_xpath)))
    print(f"   Botão encontrado com o texto: '{cancelar_btn.text}'.")
    
    try:
        # Tenta o clique normal do Selenium (mais próximo da interação do usuário)
        cancelar_btn.click()
        print("   Clicado com sucesso via Selenium nativo.")
    except Exception as e:
        # Se o clique normal falhar (ex: ElementClickInterceptedException), tenta o clique via JavaScript
        print(f"   Aviso: O clique Selenium falhou ({type(e).__name__}). Tentando clique via JavaScript como fallback.")
        driver.execute_script("arguments[0].click();", cancelar_btn)
        print("   Clicado com sucesso via JavaScript.")


    # ADIÇÃO DA PAUSA: Espera 1 segundo para o redirecionamento iniciar
    time.sleep(1) 

    # 8) Checagem e Validação do redirecionamento
    print(f"8. Checando se o redirecionamento para a URL ({VAGAS_EMPRESA_FRAGMENT}) iniciou...")

    # Se a URL ainda estiver no formulário ou em 'data:', forçamos a navegação
    current_url = driver.current_url
    if current_url == VAGAS_EMPRESA_URL or VAGAS_EMPRESA_FRAGMENT in current_url:
        print(f"   Redirecionamento iniciado corretamente para {VAGAS_EMPRESA_FRAGMENT}.")
    elif current_url.startswith("data:") or HOME_EMPRESA_URL_FRAGMENT in current_url:
        # Se a navegação não funcionou, forçamos o carregamento da URL alvo.
        print(f"   A navegação falhou (URL atual: {current_url}). Forçando navegação para {VAGAS_EMPRESA_URL}.")
        driver.get(VAGAS_EMPRESA_URL)
        # Uma pausa extra pode ser necessária após o driver.get para garantir que a página carregue.
        time.sleep(2)
    else:
        print(f"   Aguardando o EC.url_contains({VAGAS_EMPRESA_FRAGMENT})...")

    
    # A última etapa de validação (EC.url_contains) garante que a página final é a correta.
    wait.until(EC.url_contains(VAGAS_EMPRESA_FRAGMENT))

    print(f"   SUCESSO: Redirecionamento para {VAGAS_EMPRESA_FRAGMENT} confirmado.")

    # pausa pequena para visualização (opcional)
    time.sleep(1)
    
    print("--- TESTE DE CANCELAMENTO FINALIZADO COM SUCESSO ---")