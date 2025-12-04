import pytest
from testes.pages.login_page import LoginPage
from testes.pages.home_admin_page import HomeAdminPage

@pytest.mark.usefixtures("setup_driver")
class TestLogoutAdmin:
    
    def test_logout_admin(self, base_url):
        # Login
        login = LoginPage(self.driver)
        login.abrir(base_url) # Passando a URL corretamente
        login.fazer_login("fulanoadmnato@sara.com", "admin123")
        
        # Logout
        home = HomeAdminPage(self.driver)
        home.fazer_logout()
        
        # Validação
        assert "/login" in self.driver.current_url
