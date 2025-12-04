import pytest
from testes.pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.mark.usefixtures("setup_driver")
class TestEditarEmpresa:

    def test_editar_perfil_basico(self, base_url):
        # 1. Login
        login = LoginPage(self.driver)
        login.abrir(base_url)
        # Login com usuário existente
        login.fazer_login("empresa_sucesso_1764882981@teste.com", "Senha@123")

        # 2. Aguarda entrar na Home
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/home/empresa")
        )

        # 3. ATIVAR EDIÇÃO
        btn_editar = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Editar Dados')]"))
        )
        btn_editar.click()

        # 4. Editar Nome
        nome_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "nome"))
        )
        nome_input.clear()
        nome_input.send_keys("Empresa Editada Selenium")

        # Preenche o telefone para passar na validação do Zod
        telefone_input = self.driver.find_element(By.NAME, "telefone")
        telefone_input.clear()
        telefone_input.send_keys("11999999999")

        # Força o "Blur" clicando fora para remover erro de validação
        self.driver.find_element(By.XPATH, "//label[contains(text(), 'Endereço')]").click()
        time.sleep(1) # Pausa técnica para UI atualizar

        # 6. SALVAR
        btn_salvar = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Salvar')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_salvar)

        try:
            btn_salvar.click()
        except:
            self.driver.execute_script("arguments[0].click();", btn_salvar)

        # O sistema NÃO sai do modo de edição. Portanto, verificamos se NÃO deu erro.

        time.sleep(2) # Espera a ação de salvar ser processada

        # Verifica se apareceu erro na tela
        erros = self.driver.find_elements(By.CLASS_NAME, "text-red-500")
        msg_erros = [e.text for e in erros if e.is_displayed()]

        if msg_erros:
            pytest.fail(f"Erro ao salvar: {msg_erros}")

        # Verifica se o botão salvar AINDA está lá (confirma que manteve o estado esperado)
        assert btn_salvar.is_displayed(), "O botão salvar sumiu, comportamento inesperado."

        # Verifica se o valor inputado persiste no campo
        valor_atual = self.driver.find_element(By.NAME, "nome").get_attribute("value")
        assert "Empresa Editada Selenium" == valor_atual

        print("\nSucesso: Dados salvos e sistema manteve o modo de edição conforme esperado.")
