import pytest
import time
from testes.pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("setup_driver")
class TestEditarEmpresaCT026:

    EMAIL_TESTE = "empresa_sucesso_1764882981@teste.com"
    SENHA_TESTE = "Senha@123"

    def _ir_para_edicao(self, base_url):
        """Método auxiliar para logar e abrir o modo de edição"""
        login = LoginPage(self.driver)
        login.abrir(base_url)
        login.fazer_login(self.EMAIL_TESTE, self.SENHA_TESTE)

        WebDriverWait(self.driver, 10).until(EC.url_contains("/home/empresa"))

        btn_editar = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Editar Dados')]"))
        )
        btn_editar.click()

        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Salvar')]"))
        )

    # CT-026-01: Caminho Feliz
    def test_ct026_01_editar_sucesso(self, base_url):
        self._ir_para_edicao(base_url)

        novo_nome = f"Empresa Editada {int(time.time())}"

        self.driver.find_element(By.NAME, "nome").clear()
        self.driver.find_element(By.NAME, "nome").send_keys(novo_nome)

        tel = self.driver.find_element(By.NAME, "telefone")
        tel.clear()
        tel.send_keys("11999999999")

        self.driver.find_element(By.NAME, "endereco").click()
        time.sleep(0.5)

        btn_salvar = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Salvar')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_salvar)
        try:
            btn_salvar.click()
        except:
            self.driver.execute_script("arguments[0].click();", btn_salvar)

        time.sleep(2)
        erros = self.driver.find_elements(By.CLASS_NAME, "text-red-500")
        msg_erros = [e.text for e in erros if e.is_displayed()]
        assert not msg_erros, f"Erro ao salvar: {msg_erros}"

        valor_atual = self.driver.find_element(By.NAME, "nome").get_attribute("value")
        assert valor_atual == novo_nome

    # CT-026-02 (Campos Vazios) e CT-026-03 (Formatação Inválida)
    @pytest.mark.parametrize("campo, valor_invalido, mensagem_esperada", [
        ("nome", "", "Razão social obrigatória"),
        ("endereco", "", "Endereço obrigatório"),
        ("email", "emailinvalido", "Email inválido"),
        ("biografia", "curto", "10 caracteres"),
        ("telefone", "11", "Formato inválido"),
    ])
    def test_ct026_02_03_validacoes_negativas(self, base_url, campo, valor_invalido, mensagem_esperada):
        self._ir_para_edicao(base_url)

        elemento = self.driver.find_element(By.NAME, campo)
        elemento.clear()
        elemento.send_keys(valor_invalido)

        self.driver.find_element(By.NAME, "links").click()

        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Salvar')]").click()
        except:
            pass
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{mensagem_esperada}')]"))
        )
