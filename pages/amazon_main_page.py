from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonMainPage:
    """Amazon Japan Main Page 요소와 동작 관리하는 클래스"""

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.amazon.co.jp/"

        # 1. 요소를 찾는 방법 (Locators)을 변수로 저장
        self.search_box = (By.ID, "twotabsearchtextbox")
        self.search_button = (By.ID, "nav-search-submit-button")

    def open(self):
        """Amazon Main Page 접속"""
        self.driver.get(self.url)

    def search_product(self, text):
        """Product Search 수행"""
        # 안정성 향상을 위해, 10초 대기
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.presence_of_element_located(self.search_box))

        # 검색어 입력 및 버튼 클릭
        search_input.clear()
        search_input.send_keys(text)
        self.driver.find_element(*self.search_button).click()