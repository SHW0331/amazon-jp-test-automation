import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ProductDetailPage:
    def __init__(self, driver):
        self.driver = driver

        # -------------------------------------------------------
        # [Locators] 요소 정의
        # -------------------------------------------------------
        # 상품 제목 (페이지 진입 확인용) id = productTitle
        self.product_title = (By.ID, "productTitle")
        
        # 장바구니 담기 버튼 id = add-to-cart-button
        # 장바구니 담기 버튼 span[id='submit.add-to-cart-announce']
        # self.add_to_cart_button = (By.ID, "add-to-cart-button")
        # submit.add-to-cart-announce
        self.add_to_cart_button = (By.ID, "submit.add-to-cart-announce")

        # 장바구니 담기 개수 id = nav-cart-count
        self.cart_count_badge = (By.ID, "nav-cart-count")
        # 장바구니 담기 성공 메세지 id = nav-cart-count
        self.success_message = (By.XPATH, "//h1[normalize-space()='カートに入れました']")

    def get_title(self):
        """상품 상세 페이지의 제목 텍스트 추출"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.product_title)
            )
            return element.text.strip()
        except TimeoutException:
            return ""

    def add_to_cart(self):
        """장바구니 담기 버튼 클릭 및 팝업 처리"""
        try:
            # 1. 버튼이 클릭 가능할 때까지 기다렸다가 클릭
            btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.add_to_cart_button)
            )
            btn.click()

            # 2. 자바스크립트로 강제 클릭 실행 (hidden 속성)
            self.driver.execute_script("arguments[0].click();", btn)
            print(" >> [JS Click] 장바구니 버튼 강제 클릭 성공")

        except Exception as e:
            print(f"    [Error] 장바구니 담기 실패: {e}")

    def is_added_successful(self):
        """장바구니 숫자가 0보다 커졌는지, 또는 성공 메세지 확인"""
        try:
            count_elem = self.driver.find_element(*self.cart_count_badge)
            count = int(count_elem.text)
            if count > 0:
                return True

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((self.success_message))
            )
            return True

        except:
            return False

