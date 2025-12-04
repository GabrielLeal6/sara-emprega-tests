import pytest
from testes.pages.login_page import LoginPage
from testes.pages.home_admin_page import HomeAdminPage
from testes.pages.admin_approval_page import AdminApprovalPage
from testes.pages.empresa_details_page import EmpresaDetailsPage

@pytest.mark.usefixtures("setup_driver")
class TestAprovacaoEmpresa:

    def test_validar_dados_e_aprovar(self, base_url):
        login = LoginPage(self.driver)
        login.abrir(base_url)
        login.fazer_login("fulanoadmnato@sara.com", "Senha@123")

        home = HomeAdminPage(self.driver)

        approval = AdminApprovalPage(self.driver)
        nome_alvo = "Empresa Teste"

        # CT-034-03: Validar Dados
        if approval.buscar_empresa(nome_alvo):
            approval.ver_detalhes(nome_alvo)
            details = EmpresaDetailsPage(self.driver)
            dados = details.obter_dados_apresentados()

            print(f"Validando dados: {dados}")
            assert nome_alvo in dados['nome']

            # CT-034-01: Aprovar
            approval.aprovar_empresa(nome_alvo)
            print("Empresa aprovada com sucesso.")
        else:
            pytest.skip("Nenhuma empresa pendente encontrada para teste.")

        home.fazer_logout()
