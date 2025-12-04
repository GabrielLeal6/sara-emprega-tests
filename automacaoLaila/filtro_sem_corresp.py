# Comando para rodar: pytest automacaoLaila/filtro_sem_corresp.py

'''
Esse caso de teste corresponde à 
filtragem de vagas sem resultado
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

def test_filtrar_vaga_sem_resultado(setup_browser):
    driver = setup_browser
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    CIDADE_FILTRO = "Sirinhaém"
    MENSAGEM_NAO_ENCONTRADA = "Nenhuma vaga encontrada com os filtros atuais."

    print(f"\n--- INICIANDO TESTE: Filtragem sem Resultado (Cidade: {CIDADE_FILTRO}) ---")

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

    # 7) Clicar no ícone de Funil (Filtro) para abrir o modal de filtros
    print("7. Buscando e clicando no ícone de filtro (Funil) para abrir as opções...")
    filtro_btn_xpath = "//button[./*[name()='svg' and contains(@class, 'lucide-funnel')]]" 
    
    try:
        filtro_btn = wait.until(EC.element_to_be_clickable((By.XPATH, filtro_btn_xpath)))
        filtro_btn.click()
        print("7.1. Ícone de Funil (Filtro) clicado com sucesso.")
    except TimeoutException:
         raise AssertionError("Falha: O botão de filtro (ícone de funil) não foi encontrado ou não está clicável.")

    time.sleep(1) # Aguarda o modal de filtro abrir

    # 8) Marcar o filtro 'Sirinhaém'
    label_cidade_xpath = f"//label[normalize-space()='{CIDADE_FILTRO}']"
    print(f"8.1. Buscando e clicando na label para: '{CIDADE_FILTRO}'...")
    try:
        label_cidade = wait.until(EC.element_to_be_clickable((By.XPATH, label_cidade_xpath)))
        label_cidade.click()
        print(f"8.1. Cidade '{CIDADE_FILTRO}' marcada com sucesso.")
    except TimeoutException:
        raise AssertionError(f"Falha: O elemento para '{CIDADE_FILTRO}' não foi encontrado ou não está clicável.")
    
    time.sleep(1) # Aguarda a aplicação do filtro

    # 9) Validar resultado: A mensagem de "Nenhuma vaga encontrada" deve aparecer
    
    resultado_vazio_xpath = f"//div[normalize-space()='{MENSAGEM_NAO_ENCONTRADA}']"
    print(f"9. Aguardando a mensagem de '{MENSAGEM_NAO_ENCONTRADA}' aparecer...")
    
    try:
        # Timeout para carregar o resultado da filtragem
        wait_long = WebDriverWait(driver, 60) 
        resultado_vazio = wait_long.until(EC.visibility_of_element_located((By.XPATH, resultado_vazio_xpath)))
        print(f"   SUCESSO: Encontrada a mensagem de resultado vazio: '{resultado_vazio.text}'.")
    except TimeoutException:
        # Se a mensagem não aparecer, significa que uma vaga apareceu, ou o elemento não foi carregado.
        raise AssertionError(f"Falha: A mensagem de resultado vazio ('{MENSAGEM_NAO_ENCONTRADA}') não apareceu. Alguma vaga foi encontrada ou o elemento de feedback falhou. Timeout de 60s.")

    time.sleep(2)
    
    print("--- TESTE DE FILTRAGEM SEM RESULTADO FINALIZADO COM SUCESSO ---")
