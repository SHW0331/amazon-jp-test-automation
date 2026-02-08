import time
from selenium.common import NoSuchElementException, TimeoutException
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

        # 3. 배송지 변경
        self.loc_icon = (By.ID, "nav-global-location-popover-link")
        self.zip_input_front = (By.ID, "GLUXZipUpdateInput_0")
        self.zip_input_back = (By.ID, "GLUXZipUpdateInput_1")
        self.update_btn = (By.ID, "GLUXZipUpdate")
        self.done_btn = (By.ID, "GLUXConfirmClose")

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


    def set_delivery_location(self, zip_code=["100", "0001"]):
        """
        배송지 우편번호를 변경하여 지역락(구매 불가) 해제
        """
        print(f"    >> 배송지 변경 시작 (Target: {zip_code}")
        try:
            # 1. 배송지 아이콘 클릭
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.loc_icon)
            ).click()
            time.sleep(2)

            # 2. 우편번호 입력
            input_front_box = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.zip_input_front)
            )
            input_front_box.clear()
            input_front_box.send_keys(zip_code[0])

            input_back_box = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.zip_input_back)
            )
            input_back_box.clear()
            input_back_box.send_keys(zip_code[1])

            # 3. 적용 버튼
            self.driver.find_element(*self.update_btn).click()
            time.sleep(1)

            # 4. 확인 버튼
            print("     >> [Popup] 확인 (Done) 버튼 대기 중...")
            try:
                done_buttons = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(self.done_btn)
                )

                clicked = False

                for btn in done_buttons:
                    if btn.is_displayed():
                        print("     >> [Found] 실제 보이는 버튼 발견!")
                        btn.click()
                        clicked = True
                        break
                if not clicked:
                    print("     >> [Warning] 버튼들은 보이지 않음")

            except TimeoutException:
                print("     >> [Popup] 확인 버튼이 없거나 이미 닫힘 (Pass)")
                pass

            # 새로 고침
            time.sleep(2)
            self.driver.refresh()
            print(f"    >> 배송지 변경 완료 (Target: {zip_code[0]}-{zip_code[1]})")

        except Exception as e:
            print(f"    [Warning] 배송지 변경 중 오류: {e}")
