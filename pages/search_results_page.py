from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchResultsPage:
    """검색 결과 페이지의 요소와 동작을 관리하는 클래스"""

    def __init__(self, driver):
        self.driver = driver
        # 검색 결과 상품들의 공통 제목 부분
        # h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal span
        self.product_titles = (By.CSS_SELECTOR, "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal span")

    def get_all_product_titles(self):
        """검색 결과 페이지의 모든 상품 제목을 리스트로 반환"""
        elements = self.driver.find_elements(*self.product_titles)
        # 각 요소에서 text만 추출
        titles = [el.text for el in elements if el.text.strip() != ""]
        return titles

