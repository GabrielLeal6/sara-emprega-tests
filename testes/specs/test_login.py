import pytest
from testes.pages.login_page import LoginPage

@pytest.mark.usefixtures("setup_driver")
class TestLogin:
    
    def test_login_sucesso(self, base_url):
        page = LoginPage(self.driver)
        # Passa a URL explicitamente
        page.abrir(base_url)
        # Use credenciais VÁLIDAS do seu ambiente
        page.fazer_login("fulanoadmnato@sara.com", "admin123")
        
        assert page.esta_na_home(), "Não redirecionou para home após login"

    def test_login_senha_invalida(self, base_url):
        page = LoginPage(self.driver)
        page.abrir(base_url)
        page.fazer_login("fulanoadmnato@sara.com", "SenhaErrada")
        
        msg = page.obter_mensagem_erro_global()
        assert msg is not None, "Deveria ter aparecido erro global"

    def test_login_email_inexistente(self, base_url):
        page = LoginPage(self.driver)
        page.abrir(base_url)
        page.fazer_login("naoexiste@sara.com", "Senha@123")
        
        msg = page.obter_mensagem_erro_global()
        assert msg is not None

    def test_login_campos_vazios(self, base_url):
        page = LoginPage(self.driver)
        page.abrir(base_url)
        page.fazer_login("", "")
        
        assert "/login" in self.driver.current_url

    def test_login_conta_inativa(self, base_url):
        page = LoginPage(self.driver)
        page.abrir(base_url)
        page.fazer_login("inativo@teste.com", "Senha@123")
        
        msg = page.obter_mensagem_erro_global()
        if not msg:
            assert "/home" not in self.driver.current_url
