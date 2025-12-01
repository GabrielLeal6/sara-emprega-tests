"""TESTE CT001.03 Login com e-mail inexistente. """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

# NOTE
CHROME_DRIVER_PATH = '/path/to/chromedriver'
LOGIN_URL = 'http://localhost:3000/login' 

# Test Credentials
VALID_EMAIL = 'teste@mail.com'
VALID_PASSWORD = 'senha123'

def setup_driver():
    """Initializes and configures the Selenium WebDriver."""
    try:

        if CHROME_DRIVER_PATH and CHROME_DRIVER_PATH != '/path/to/chromedriver':
             service = Service(CHROME_DRIVER_PATH)
             driver = webdriver.Chrome(service=service)
        else:
            driver = webdriver.Chrome()
        
        return driver
    except WebDriverException as e:
        print(f"Error setting up WebDriver: {e}")
        print("Please ensure ChromeDriver is installed and its path is correctly configured.")
        return None

def test_login_success(driver):
    """
    Automates the steps to log in to the application.
    1. Access the Login screen.
    2. Insert a valid email.
    3. Insert a valid password.
    4. Click the 'Entrar' button.
    """
    
    print(f"1.  Accessing URL: {LOGIN_URL}")
    driver.get(LOGIN_URL)

    time.sleep(2) 
    
    try:
        email_field = driver.find_element(By.CSS_SELECTOR, 'input[type="email"], input:nth-of-type(1)')
        print(f"2.  Inserting Email: {VALID_EMAIL}")
        email_field.send_keys(VALID_EMAIL)
        

        password_field = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
        print(f"3.  Inserting Password: {'*' * len(VALID_PASSWORD)}")
        password_field.send_keys(VALID_PASSWORD)
        

        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        print("4.  Clicking 'Entrar' button...")
        login_button.click()


        print("5.  Login action completed. Waiting for redirection/result...")
        time.sleep(3)
        
        current_url = driver.current_url
        if current_url != LOGIN_URL:
            print(f"Success! Driver was redirected to: {current_url}")
        else:
            print("Warning: Still on the login page. Login may have failed or there was no redirection.")

    except NoSuchElementException:
        print("Test FAILED: One or more required elements (Email/Password fields or 'Entrar' button) were not found on the page.")
    except Exception as e:
        print(f"An unexpected error occurred during the test: {e}")


if __name__ == "__main__":
    driver = setup_driver()
    
    if driver:
        try:
            test_login_success(driver)
        finally:
            print("\nTest finished. Closing the browser in 5 seconds...")
            time.sleep(5)
            driver.quit()