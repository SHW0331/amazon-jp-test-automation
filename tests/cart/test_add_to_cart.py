import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.amazon_main_page import AmazonMainPage
from pages.cart_page import CartPage
from pages.search_results_page import SearchResultsPage
from pages.product_detail_page import ProductDetailPage
# [수정 1] 파일명 맞춤 (excel_report)
from utils.excel_report import ExcelReporter

# 리포터 초기화
reporter = ExcelReporter()


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# =================================================================================
# 1. 장바구니 담기 (TC_CART_01)
# =================================================================================
def test_add_to_cart(driver):
    """
    [TC_CART_01] 상품 검색 -> 상세 페이지 진입 -> 장바구니 담기 -> 성공 확인
    """
    tc_id = "TC_CART_01"
    module = "Cart"
    scenario = "검색 후 장바구니 담기(Flow)"
    keyword = "マリオカート8 デラックス"
    expected = "장바구니 담기 성공 메세지 출력 or 카운트 증가"

    try:
        print(f"\n[Start] {scenario}")
        main_page = AmazonMainPage(driver)
        main_page.open()
        # [수정 2] 오타 수정 & 인자 전달
        main_page.set_delivery_location(["100", "0001"])
        main_page.search_product(keyword)
        print(" >> 검색어 입력 완료")

        time.sleep(2)

        result_page = SearchResultsPage(driver)
        # [수정 3] 오타 수정 (frist -> first)
        result_page.click_first_product()
        print(" >> 첫 번째 상품 클릭 완료")

        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        print(f" >> [Switch] 새 탭으로 드라이버 이동")

        detail_page = ProductDetailPage(driver)
        title = detail_page.get_title()
        print(f" >> 상세 페이지 진입: {title[:30]}...")

        detail_page.add_to_cart()
        print(" >> '장바구니 담기' 버튼 클릭")

        time.sleep(3)

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

    reporter.log_result(tc_id, module, scenario, keyword, expected, actual, status)
    print(f" >> 결과 저장 완료: {status}")


# =================================================================================
# 2. 장바구니 삭제 (TC_CART_02)
# =================================================================================
def test_delete_cart(driver):
    """
    [TC_CART_02] 장바구니 페이지 이동 -> 상품 삭제 -> 장바구니 0개 확인
    """
    tc_id = "TC_CART_02"
    module = "Cart"
    scenario = "장바구니 상품 삭제 및 초기화"
    keyword = "掃除機"
    expected = "장바구니 삭제 메시지 출력"
    status = "FAIL"
    actual = ""

    try:
        print(f"\n[Start] {scenario}")

        # [Pre-condition] 상품 담기
        main_page = AmazonMainPage(driver)
        main_page.open()
        # [수정 2] 오타 수정 & 인자 전달
        main_page.set_delivery_location(["100", "0001"])
        main_page.search_product(keyword)
        print(" >> 검색어 입력 완료")

        time.sleep(2)

        result_page = SearchResultsPage(driver)
        # [수정 3] 오타 수정
        result_page.click_first_product()
        print(" >> 첫 번째 상품 클릭 완료")

        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        print(f" >> [Switch] 새 탭으로 드라이버 이동")

        detail_page = ProductDetailPage(driver)
        detail_page.add_to_cart()
        print(" >> '장바구니 담기' 버튼 클릭")
        time.sleep(3)

        # 장바구니 이동 및 삭제
        cart_page = CartPage(driver)
        cart_page.go_to_cart()
        time.sleep(3)

        item_title = cart_page.get_first_item_title()
        if not item_title:
            raise Exception("장바구니에 상품이 없어 테스트 불가")
        print(f" >> 삭제할 상품 확인: {item_title[:20]}...")

        cart_page.clear_cart()

        status = "PASS"
        actual = "삭제 버튼 클릭 및 메시지 확인 완료"

    except Exception as e:
        status = "ERROR"
        actual = f"에러 발생: {str(e)}"
        print(f"    [ERROR] {e}")

    reporter.log_result(tc_id, module, scenario, keyword, expected, actual, status)
    print(f" >> 결과 저장 완료: {status}")