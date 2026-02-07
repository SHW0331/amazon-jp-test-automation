import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CartPage:
    def __init__(self, driver):
        self.driver = driver

        # 1. 상단 장바구니 아이콘 # nav-cart-icon nav-sprite
        self.nav_cart_icon = (By.ID, "nav-cart")
        # 2. 장바구니에 담긴 첫 번째 상품의 제목 # a-truncate-cut
        # span[class ='a-truncate-full a-offscreen']
        self.cart_item_title = (By.CSS_SELECTOR, ".sc-grid-item-product-title .a-truncate-full")
        # 3. 삭제(掃除) 버튼 # 'decrement-icon
        self.delete_btn = (By.CSS_SELECTOR, "span[data-a-selector$='decrement-icon']")
        # 4. 삭제 확인 메세지 # sc-list-item-removed-msg
        self.removed_msg = (By.CLASS_NAME, "sc-list-item-removed-msg")

    def go_to_cart(self):
        """상단 아이콘을 눌러 장바구니 페이지로 이동"""
        print("   >> [Action] 장바구니 아이콘 클릭 -> 이동 중...")
        self.driver.find_element(*self.nav_cart_icon).click()

    def get_first_item_title(self):
        """장바구니에 있는 첫 번째 상품의 제목 추출"""
        try:
            title_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.cart_item_title)
            )
            return title_elem.get_attribute("textContent").strip()
        except TimeoutException:
            print("   >> [Info] 장바구니에 상품이 없거나 제목을 못 찾았습니다.")

    def clear_cart(self):
        """장바구니에 있는 상품을 삭제"""
        try:
            print("   >> [Cleanup] 장바구니 비우기 시작...")

            delete_buttons = self.driver.find_elements(*self.delete_btn)
            if len(delete_buttons) > 0:
                delete_buttons[0].click()
                print("   >> [Action] '삭제(削除)' 버튼 클릭")

                removed_messages = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.removed_msg)
                )
                if removed_messages:
                    print("   >> [Success] '삭제되었습니다' 메시지 확인 완료")
            else:
                print("   >> [Info] 이미 장바구니가 비어있습니다.")
        except Exception as e:
            print(f"   [Error] 장바구니 비우기 실패: {e}")



