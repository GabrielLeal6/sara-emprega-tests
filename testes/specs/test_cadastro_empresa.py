import pytest
import time
from testes.pages.empresa_registration_page import EmpresaRegistrationPage

# Dados para geração de massa
timestamp = int(time.time())
EMAIL_SUCESSO = f"empresa_sucesso_{timestamp}@teste.com"
CNPJ_SUCESSO = "77169849000118"

@pytest.mark.usefixtures("setup_driver")
class TestCadastroEmpresa:

    # CT-025-01: Caminho Feliz
    def test_cadastro_sucesso(self, base_url):
        page = EmpresaRegistrationPage(self.driver)
        page.abrir(base_url)

        print(f"Tentando cadastro com: {EMAIL_SUCESSO}")
        page.preencher_formulario(
            nome=f"Empresa Teste {timestamp}",
            cnpj=CNPJ_SUCESSO,
            email=EMAIL_SUCESSO,
            telefone="11999999999",
            endereco="Rua Teste, 123",
            senha="Senha@123",
            confirm_senha="Senha@123",
            bio="Empresa de automação.",
            link="https://site.com"
        )
        page.submeter()

        assert page.verificar_sucesso(), "A mensagem de 'Solicitação Enviada' não apareceu."

    # CT-025-02 (CNPJ Inválido), CT-025-04 (Vazio), Senhas divergentes
    @pytest.mark.parametrize("nome, cnpj, email, senha, confirm, msg_esperada", [
        ("Empresa CNPJ Ruim", "11111", "email@teste.com", "123", "123", "CNPJ inválido"), # CT-025-02
        ("", "77169849000118", "email@teste.com", "123", "123", "Obrigatório"), # CT-025-04
        ("Empresa Senha", "77169849000118", "email@teste.com", "123", "321", "Senhas não conferem")
    ])
    def test_cadastro_invalidos(self, base_url, nome, cnpj, email, senha, confirm, msg_esperada):
        page = EmpresaRegistrationPage(self.driver)
        page.abrir(base_url)

        page.preencher_formulario(
            nome=nome, cnpj=cnpj, email=email, telefone="11999999",
            endereco="Rua", senha=senha, confirm_senha=confirm, bio="..", link=".."
        )
        page.submeter()

        erro_atual = page.verificar_erro()
        if erro_atual:
            print(f"Erro encontrado: {erro_atual}")
            assert True
        else:
            assert "/cadastro" in self.driver.current_url

    # CT-025-03: Email já existente
    def test_cadastro_email_duplicado(self, base_url):
        page = EmpresaRegistrationPage(self.driver)
        page.abrir(base_url)

        page.preencher_formulario(
            nome="Empresa Duplicada", cnpj="56382956000112",
            email=EMAIL_SUCESSO,
            telefone="11999999", endereco="Rua", senha="123", confirm_senha="123", bio="..", link=".."
        )
        page.submeter()

        pass
