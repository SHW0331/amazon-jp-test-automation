from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchResultsPage:
    """검색 결과 페이지의 요소와 동작을 관리하는 클래스"""

    def __init__(self, driver):
        self.driver = driver

        # 상품 카드(Box) loactor = div[data-cy="asin-faceout-container"]
        self.product_cards = (By.CSS_SELECTOR, "div[data-cy='asin-faceout-container']")
        # 상품 제목(title) locator = div[data-cy='title-recipe'] a h2 span
        self.title_locator = (By.CSS_SELECTOR, "div[data-cy='title-recipe'] a h2 span")
        # 상품 가격(price) locator = span[class='a-color-price']
        self.price_locator = (By.CSS_SELECTOR, "span[class='a-color-price']")
        # 광고 locator = span[class="puis-label-popover-default"]
        self.sponsored_locator = (By.CSS_SELECTOR, "span.puis-label-popover-default")

    def get_product_info_list(self):
        """상품 카드를 하나씩 순회하며 제목과 가격을 추출"""
        # 1. 화면에 있는 모든 상품 카드 추출
        cards = self.driver.find_elements(*self.product_cards)
        product_list = []

        for card in cards:
            try:
                # 2. 제목 추출 (광고 라벨이 하나라도 있으면 continue
                if len(card.find_elements(*self.sponsored_locator)) > 0:
                    continue

                title_element = card.find_element(*self.title_locator)
                title = title_element.text.strip()

                # 3. 가격 추출
                try:
                    price_element = card.find_element(*self.price_locator)
                    price = price_element.text.strip()
                except:
                    price = "N/A"

                # 4. 리스트 추가
                if title:
                    product_list.append({
                        'title': title,
                        'price': price
                    })

            except Exception:
                # 카드 하나를 읽다가 문제가 생기면 무시하고 다음 카드로
                continue

        return product_list