# Comando para rodar: pytest automacaoLaila/publicar_vaga.py
'''
Esse caso teste corresponde à publicação de uma vaga pela entidade
empresa com dados válidos em todos os campos.
'''
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


# Configurações
LOGIN_URL = "https://sara-frontend-736daffd516a.herokuapp.com/login"
HOME_EMPRESA_URL_FRAGMENT = "/home/empresa"
DEFAULT_TIMEOUT = 30 

def _select_radix_option(driver, wait: WebDriverWait, button_id: str, option_text: str, timeout_sec: int = 12):
    """
    Clica no botão do Radix combobox (pelo id) e seleciona a opção desejada.
    Prioriza o locator de 'role=option' que é comum em portais Radix.
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


def test_publicar_vaga(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    print("\n--- INICIANDO TESTE: Publicação de Vaga ---")

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


    # 5) Preencher campos de texto
    print("5. Preenchendo campos de texto...")
    
    # Campo "title"
    title = wait.until(EC.presence_of_element_located((By.ID, "title")))
    title.clear()
    title.send_keys("Desenvolvedor Front-end - Automação")

    # Campo "area"
    area = wait.until(EC.presence_of_element_located((By.ID, "area")))
    area.clear()
    area.send_keys("Tecnologia")

    # Campo "description"
    description = wait.until(EC.presence_of_element_located((By.ID, "description")))
    description.clear()
    description.send_keys("Atuação com React/Next.js e Tailwind. Vaga para estágio.")

    # Campo "requirements"
    requirements = wait.until(EC.presence_of_element_located((By.ID, "requirements")))
    requirements.clear()
    requirements.send_keys("Desejável conhecimento básico em JavaScript e React.")

    # Campo "location"
    location = wait.until(EC.presence_of_element_located((By.ID, "location")))
    location.clear()
    location.send_keys("São Paulo, SP")

    # Campo "salary"
    salary = wait.until(EC.presence_of_element_located((By.ID, "salary")))
    salary.clear()
    salary.send_keys("A combinar")
    
    # Pausa de 1 segundo para garantir que o framework de front-end registre o preenchimento de todos os inputs
    time.sleep(1)

    # 6) Selecionar Tipo -> Estágio (Radix combobox)
    _select_radix_option(driver, wait, button_id="type", option_text="Estágio")

    # 7) Selecionar Modalidade -> Presencial (Radix combobox)
    _select_radix_option(driver, wait, button_id="modality", option_text="Presencial")
    
    print("8. Pausando 1s para estabilizar o formulário antes de publicar...")
    time.sleep(1) # Pausa estratégica final

    # 9) Clicar em Publicar Vaga (Locator mais genérico)
    print("9. Tentando clicar no botão 'Publicar Vaga'...")
    
    # Usando um contains mais genérico para buscar qualquer botão que contenha "Publicar"
    publicar_xpath = "//button[contains(translate(normalize-space(.), 'PUBLICAR', 'publicar'), 'publicar')]"
    
    publicar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, publicar_xpath)))
    
    # Loga o texto exato do botão encontrado
    print(f"   Botão encontrado com o texto: '{publicar_btn.text}'. Clicando...")
    publicar_btn.click()

    # 10) Validar popup de sucesso
    print("10. Validando popup de sucesso...")
    
   
    try:
        success_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(normalize-space(.), 'Vaga Publicada')]")))
    except TimeoutException:
        print("   Aviso: H2 não encontrado. Tentando locator genérico para o título...")
        # Tentativa 2: Qualquer elemento visível
        try:
             success_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(.), 'Vaga Publicada')]")))
        except TimeoutException:
             print("   Aviso: Locator genérico falhou. Tentando locator para texto em qualquer lugar...")
             # Tentativa 3: Último recurso
             success_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//body//*[contains(normalize-space(.), 'Vaga Publicada')]")))


    # Espera pela mensagem de detalhe
    wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(.), 'Sua vaga foi cadastrada com sucesso')]")))
    
    print("   SUCESSO: Popup 'Vaga Publicada' encontrado.")

    # pausa pequena para visualização 
    time.sleep(1)
    
    print("--- TESTE FINALIZADO COM SUCESSO ---")