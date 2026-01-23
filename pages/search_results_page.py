import time

from selenium.common import NoSuchDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchResultsPage:
    """검색 결과 페이지의 요소와 동작을 관리하는 클래스"""

    def __init__(self, driver):
        self.driver = driver

        # [1] 상품 카드 & 내부 요소
        # 상품 카드(Box) loactor = div[data-cy="asin-faceout-container"]
        self.product_cards = (By.CSS_SELECTOR, "div[data-cy='asin-faceout-container']")
        # 상품 제목(title) locator = div[data-cy='title-recipe'] a h2 span
        self.title_locator = (By.CSS_SELECTOR, "div[data-cy='title-recipe'] a h2 span")
        # 상품 가격(price) locator = span[class='a-color-price']
        self.price_locator = (By.CSS_SELECTOR, "span[class='a-color-price']")
        # 광고 locator = span[class="puis-label-popover-default"]
        self.sponsored_locator = (By.CSS_SELECTOR, "span[class='puis-label-popover-default']")

        # [2] page locator
        # 다음 버튼(next button) locator = a.s-pagination-next
        self.next_btn = (By.CSS_SELECTOR, "a.s-pagination-next")

    def get_product_info_list(self):
        """상품 카드를 하나씩 순회하며 제목과 가격을 추출"""
        # 1. 화면에 있는 모든 상품 카드 추출
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(*self.product_cards)
        )
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

    def click_next_page(self):
        """다음 페이지 클릭, 성공 True, 버튼이 없으면 False 반환"""
        try:
            button = self.driver.find_element(*self.next_btn)

            # 버튼 활성화 확인 <a>, <span>이면 마지막 페이지
            if button.tag_name == "a":
                button.click()
                time.sleep(2)
                return True
            else:
                return False

        except Exception:
            return False

    def click_frist_product(self):
        """검색 결과의 첫 번째 상품을 클릭"""
        """스폰서 상품 건너뛰기"""
        print("     >> [Filter] 스폰서(광고) 상품 제외하고 탐색 시작...")

        # 1. 모든 결과 항목 가져오기
        # (로딩 대기: 결과가 최소 1개 뜰 때까지)
        cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(self.product_cards)
        )

        found = False

        for index, card in enumerate(cards):
            try:
                if len(card.find_elements(*self.sponsored_locator)) > 0:
                    print(f"    -[Skip] {index+1}번째 상품은 광고")
                    continue
                print(f"     - [Found] {index + 1}번째 상품이 진짜입니다!")
                title_elem = card.find_element(*self.title_locator)
                print(f"       (Title: {title_elem.text[:30]}...)")

                title_elem.click()
                found = True
                break

            except Exception as e:
                print(f"    [Warning] 카드 처리 중 에러 : {e}")
                continue

        if not found:
            raise Exception("광고 제외 후 클릭할 상품을 찾지 못함")

        # first_item = self.driver.find_element(*self.title_locator)
        # first_item.click()