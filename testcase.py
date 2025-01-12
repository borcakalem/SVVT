import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class HerokuAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Safari()
        cls.driver.maximize_window()
        cls.base_url = "https://the-internet.herokuapp.com/"

    def setUp(self):
        self.driver.get(self.base_url)

    # Scenario 1: User Authentication
    def test_valid_login(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.success"))
        )
        self.assertIn("You logged into a secure area!", success_message.text)
        print("Successful login")

    def test_invalid_login(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("user")
        self.driver.find_element(By.ID, "password").send_keys("pass")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.error"))
        )
        self.assertIn("Your username is invalid!", error_message.text)
        print("Invalid login")

    def test_empty_login_fields(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.error"))
        )
        self.assertIn("Your username is invalid!", error_message.text)
        print("invalid login")

    # Scenario 2: Navigation
    def test_navigation_links(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.LINK_TEXT, "Checkboxes").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Broken Images").click()
        time.sleep(1)
        self.driver.back()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Dropdown").click()

    # Scenario 3: Form Validations
    def test_form_submission_valid(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        success_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.success"))
        )
        self.assertIn("You logged into a secure area!", success_message.text)

    def test_form_submission_invalid(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("user")
        self.driver.find_element(By.ID, "password").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.error"))
        )
        self.assertIn("Your username is invalid!", error_message.text)

    # Scenario 4: Static Content
    def test_static_content_presence(self):
        header = self.driver.find_element(By.TAG_NAME, "header")
        footer = self.driver.find_element(By.TAG_NAME, "footer")
        self.assertIsNotNone(header, "Header is missing.")
        self.assertIsNotNone(footer, "Footer is missing.")

    # Scenario 5: Edge Cases
    def test_special_characters_in_input(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("!%^%^&&*()")
        self.driver.find_element(By.ID, "password").send_keys("!@^%^&*()")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.error"))
        )
        self.assertIn("Your username is invalid!", error_message.text)

    # Scenario 6: Responsiveness
    def test_responsive_design(self):
        self.driver.set_window_size(375, 812)  # iPhone 13
        self.driver.get(self.base_url)
        menu_button = self.driver.find_element(By.CLASS_NAME, "menu-toggle")
        self.assertTrue(menu_button.is_displayed(), "Responsive menu is not displayed.")

    # Scenario 7: Logout Functionality
    def test_logout(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "a[href='/logout']").click()
        page_header = self.driver.find_element(By.TAG_NAME, "h2").text
        time.sleep(1)

    # Scenario 8: Session Management
    def test_session_persistence_on_refresh(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        self.driver.refresh()
        self.assertIn("Secure Area", self.driver.page_source, "Session did not persist")

    # Scenario 9: API Behavior
    def test_dynamic_content_api_response(self):
        self.driver.get(f"{self.base_url}/dynamic_content")
        content = self.driver.find_element(By.CLASS_NAME, "example").text
        time.sleep(2)
        self.assertTrue(content, "Dynamic content did not load properly.")

    # Scenario 10: Page Load Performance
    def test_page_load_time(self):
        start_time = time.time()
        self.driver.get(f"{self.base_url}/login")
        load_time = time.time() - start_time
        self.assertLess(load_time, 3, f"Page load time is too long: {load_time} seconds")

    # Scenario 11: 404 Error Page
    def test_404_error_page(self):
        self.driver.get(f"{self.base_url}/nonexistent_page")
        error_message = self.driver.find_element(By.TAG_NAME, "h1").text
        time.sleep(1)
        self.assertIn("Not Found", error_message, "404 error page not displayed properly.")

    # Scenario 12: File Upload
    def test_file_upload(self):
        self.driver.get(f"{self.base_url}/upload")
        file_input = self.driver.find_element(By.ID, "file-upload")
        file_input.send_keys("/Users/alemborcak/PycharmProjects/PythonProject/image.webp")
        time.sleep(1)
        self.driver.find_element(By.ID, "file-submit").click()
        time.sleep(4)
        uploaded_file = self.driver.find_element(By.ID, "uploaded-files").text
        self.assertIn("image.webp", uploaded_file, "File upload failed.")

    # Scenario 13: File Download
    def test_file_download(self):
        self.driver.get(f"{self.base_url}/download")
        download_link = self.driver.find_element(By.CSS_SELECTOR, "a[href*='download']")
        download_link.click()
        time.sleep(5)

    # Scenario 14: CAPTCHA Validation
    def test_captcha_validation(self):
        self.driver.get(f"{self.base_url}/captcha")
        self.driver.find_element(By.ID, "username").send_keys("usr")
        self.driver.find_element(By.ID, "password").send_keys("pass")
        self.driver.find_element(By.ID, "submit-btn").click()
        time.sleep(2)

    # Scenario 15: Security Tests
    def test_sql_injection(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "username").send_keys("' OR '1'='1")
        self.driver.find_element(By.ID, "password").send_keys("passwd")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "flash.error"))
        )
        self.assertIn("Your username is invalid!", error_message.text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
