import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.amazon_main_page import AmazonMainPage
from pages.search_results_page import SearchResultsPage
from pages.product_detail_page import ProductDetailPage
from utils.excel_reporter import ExcelReporter

# 리포터 초기화
reporter = ExcelReporter()

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_add_to_cart(driver):
    """
        [TC_CART_01] 상품 검색 -> 상세 페이지 진입 -> 장바구니 담기 -> 성공 확인
        """
    # ----------------------------------------------------------
    # 1. 테스트 데이터 정의
    # ----------------------------------------------------------
    tc_id = "TC_CART_01"
    module = "Cart"
    scenario = "검색 후 장바구니 담기(Flow)"
    keyword = "マリオカート8 デラックス"
    expected = "장바구니 담기 성공 메세지 출력 or 카운트 증가"

    try:
        # ------------------------------------------------------
        # 2. 메인 페이지 -> 검색
        # ------------------------------------------------------
        print(f"\n[Start] {scenario}")
        main_page = AmazonMainPage(driver)
        main_page.open()
        main_page.set_dlivery_location()
        main_page.search_product(keyword)
        print(" >> 검색어 입력 완료")

        time.sleep(2)

        # ------------------------------------------------------
        # 3. 검색 결과 -> 첫 번째 상품 클릭
        # ------------------------------------------------------
        result_page = SearchResultsPage(driver)
        result_page.click_frist_product()
        print(" >> 첫 번째 상품 클릭 완료")

        # ------------------------------------------------------
        # 4. 상세 페이지 -> 장바구니 담기
        # ------------------------------------------------------
        # 새탭에서 열림
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        print(f" >> [Switch] 새 탭으로 드라이버 이동")

        detail_page = ProductDetailPage(driver)

        # (검증) 내가 들어온 페이지 제목 확인
        title = detail_page.get_title()
        print(f" >> 상세 페이지 진입: {title[:30]}...")

        # 장바구니 버튼 클릭!
        detail_page.add_to_cart()
        print(" >> '장바구니 담기' 버튼 클릭")

        time.sleep(3)

        # ------------------------------------------------------
        # 5. 결과 검증 (성공 메시지 or 카운트 확인)
        # ------------------------------------------------------
        is_success = detail_page.is_added_successful()

        if is_success:
            status = "PASS"
            actual = "장바구니 담기 성공"
        else:
            status = "FAIL"
            actual = "성공 메시지가 뜨지 않음"

    except Exception as e:
        status = "ERROR"
        actual = f"에러 발생: {str(e)}"
        print(f"    [ERROR] {e}")

    # ----------------------------------------------------------
    # 6. 리포트 저장
    # ----------------------------------------------------------
    reporter.log_result(tc_id, module, scenario, keyword, expected, actual, status)
    print(f" >> 결과 저장 완료: {status}")
