# Comando para rodar: pytest automacaoLaila/publicar_vaga_vazio.py
'''
Esse caso de teste corresponde à
tentativa de publicação de vaga sem preencher os campos obrigatórios
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
DEFAULT_TIMEOUT = 30 

def _select_radix_option(driver, wait: WebDriverWait, button_id: str, option_text: str, timeout_sec: int = 12):
    """
    Função auxiliar removida para este teste, pois não irá preencher os campos.
    Ela havia sido usada nos outros testes.
    """
    pass

def test_tentar_publicar_vaga_sem_preencher(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    print("\n--- INICIANDO TESTE: Tentativa de Publicação sem Preenchimento ---")

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

    # 5) Verificar se está na URL correta antes do clique
    initial_url = driver.current_url
    print(f"5. URL inicial: {initial_url}")
    
    
    # 6) Clicar em Publicar Vaga (Locator mais genérico)
    print("6. Tentando clicar no botão 'Publicar Vaga' SEM PREENCHER NADA...")
    
    # Usando um contains mais genérico para buscar qualquer botão que contenha "Publicar"
    publicar_xpath = "//button[contains(translate(normalize-space(.), 'PUBLICAR', 'publicar'), 'publicar')]"
    
    publicar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, publicar_xpath)))
    
    print(f"   Botão encontrado com o texto: '{publicar_btn.text}'. Clicando...")
    publicar_btn.click()

    # 7) Validar que a URL NÃO mudou (permanece na mesma página de formulário)
    # Se o formulário não for validado, não deve haver redirecionamento.
    print("7. Validando que a URL não mudou após o clique...")
    time.sleep(2) # Pausa para o potencial redirecionamento ou aviso de erro
    
    current_url = driver.current_url
    
    if current_url != initial_url:
        raise AssertionError(f"Falha: Ocorreu um redirecionamento inesperado! A URL mudou de '{initial_url}' para '{current_url}'.")
    
    print("   SUCESSO: A URL PERMANECEU a mesma após a tentativa de publicação (indicando falha na validação).")

    # 8) Validar AUSÊNCIA do popup de sucesso
    # O teste SÓ passa se o elemento NÃO for encontrado.
    print("8. Validando AUSÊNCIA do popup 'Vaga Publicada'...")
    try:
        # Tenta encontrar o título do popup de sucesso
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(normalize-space(.), 'Vaga Publicada')]")))
        # Se o código chegar aqui, significa que o popup APARECEU, o que é uma falha no teste
        raise AssertionError("Falha Crítica: O popup 'Vaga Publicada' foi exibido mesmo com campos vazios.")
    except TimeoutException:
        # Este é o comportamento esperado: o popup NÃO deve ser encontrado
        print("   SUCESSO: O popup 'Vaga Publicada' NÃO foi exibido (comportamento esperado).")
    
    time.sleep(2)
    
    print("--- TESTE DE PUBLICAÇÃO SEM PREENCHIMENTO FINALIZADO COM SUCESSO ---")
