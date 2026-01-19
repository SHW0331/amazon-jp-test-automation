from selenium.common import NoSuchElementException
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

        # 2. 메크로 확인
        self.continue_button = (By.XPATH, "//button[contains(text(),'ショッピングを続ける')]")

    def open(self):
        """Amazon Main Page 접속"""
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)

        # 메크로 버튼 확인
        self._handle_interstitial_page()

    def _handle_interstitial_page(self):
        """
        중간에 '쇼핑 계속하기' 같은 에러/경고 페이지 예외처리
        """
        try:
            btn = self.driver.find_element(*self.continue_button)
            if btn.is_displayed():
                print("    [Alert] 자동화 접근 감지 페이지 발견")
                btn.click()
                self.driver.implicitly_wait(2)
        except NoSuchElementException:
            pass
        except Exception as e:
            print(f"    [Warning] 예외 페이지 처리 에러: {e}")


    def search_product(self, text):
        """Product Search 수행"""
        # 안정성 향상을 위해, 10초 대기
        wait = WebDriverWait(self.driver, 10)
        search_input = wait.until(EC.presence_of_element_located(self.search_box))

        # 검색어 입력 및 버튼 클릭
        search_input.clear()
        search_input.send_keys(text)
        self.driver.find_element(*self.search_button).click()