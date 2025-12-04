import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def setup_driver(request):
    print("\n[Fixture] Inicializando Driver...")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(5)

    if request.cls:
        request.cls.driver = driver

    yield driver

    print("\n[Fixture] Finalizando Driver...")
    driver.quit()

@pytest.fixture
def base_url():
    return "https://sara-frontend-736daffd516a.herokuapp.com"
