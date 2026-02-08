import pytest
import time
import random
from selenium import webdriver
from pages.amazon_main_page import AmazonMainPage
from pages.search_results_page import SearchResultsPage
from utils.excel_report import ExcelReporter

reporter = ExcelReporter()

@pytest.fixture
def driver():
    """테스트마다 브라우저를 열고 닫음"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# =================================================================================
# 1. [Positive Test] 정상 결과 검증 (TC 01, 02, 03, 05, 07)
# =================================================================================
@pytest.mark.parametrize("tc_id, scenario, keyword", [
    # -------------------------------------------------------------------------
    # [TC_SEARCH_01] 기본 영문 검색
    # - 목적: 가장 기본적인 메인 키워드(PS5) 검색 시 상품이 정상 노출되는지 확인
    # -------------------------------------------------------------------------
    ("TC_SEARCH_01", "기본 영문 검색 (PS5)", "PS5"),

    # -------------------------------------------------------------------------
    # [TC_SEARCH_02] 다국어(일본어) 검색
    # - 목적: 일본어 입력(任天堂) 시 깨짐 없이 결과가 나오는지 확인 (로컬라이징 검증)
    # -------------------------------------------------------------------------
    ("TC_SEARCH_02", "다국어/로컬 검색 (ニンテンドースイッチ)", "ニンテンドースイッチ"),

    # -------------------------------------------------------------------------
    # [TC_SEARCH_03] 복합 키워드 검색
    # - 목적: 띄어쓰기가 포함된 긴 상품명(Nintendo Switch OLED) 처리 확인
    # -------------------------------------------------------------------------
    ("TC_SEARCH_03", "복합 키워드 검색 (Nintendo Switch OLED)", "Nintendo Switch OLED"),

    # -------------------------------------------------------------------------
    # [TC_SEARCH_05] 특수문자 포함 검색
    # - 목적: URL 인코딩이 필요한 특수문자(&)가 포함된 게임 타이틀 처리 확인
    # -------------------------------------------------------------------------
    ("TC_SEARCH_05", "특수문자 포함 검색 (PS5 & VR2)", "PS5 & VR2"),

    # -------------------------------------------------------------------------
    # [TC_SEARCH_07] 공백 자동 제거(Trim) 검색
    # - 목적: 검색어 앞뒤에 실수로 들어간 공백을 시스템이 무시하고 검색하는지 확인
    # -------------------------------------------------------------------------
    ("TC_SEARCH_07", "앞뒤 공백 자동제거 ( Xbox Series X )", "  Xbox Series X  ")
])
def test_search_positive(driver, tc_id, scenario, keyword):
    """
    [통합 테스트] 정상 검색어(TC 01, 02, 03, 05, 07) 입력 시 결과 노출 검증
    """
    module = "Search"
    expected = "상품이 1개 이상 노출"

    try:
        # 1. 메인 페이지 이동
        main_page = AmazonMainPage(driver)
        main_page.open()

        # 2. 검색 수행
        main_page.search_product(keyword)
        # Anti-Bot Wait (Random)
        time.sleep(random.uniform(2, 5))

        # 3. 결과 수집
        results_page = SearchResultsPage(driver)
        items = results_page.get_product_info_list()
        count = len(items)

        # 4. 검증 (Verify)
        actual = f"수집된 상품 개수: {count}개"
        if count > 0:
            status = "PASS"
        else:
            status = "FAIL"
            actual += " (상품이 발견되지 않음)"

    except Exception as e:
        status = "ERROR"
        actual = f"에러 발생: {str(e)}"

    # 5. 리포트 저장
    reporter.log_result(tc_id, module, scenario, keyword, expected, actual, status)


# =================================================================================
# 2. [Negative Test] 결과가 없어야 하는 케이스 (TC 04)
# =================================================================================
def test_search_negative_no_result(driver):
    """
    [TC_SEARCH_04] 존재하지 않는 키워드 검색 시 0건 확인
    - 목적: 검색 결과가 없을 때 시스템이 에러 없이 0건으로 처리하는지 확인
    """
    tc_id = "TC_SEARCH_04"
    module = "Search"
    scenario = "존재하지 않는 키워드 검색"
    keyword = "qweasdzxcasdqweasdzxc"
    expected = "수집된 상품이 0개"

    try:
        main_page = AmazonMainPage(driver)
        main_page.open()

        main_page.search_product(keyword)
        time.sleep(random.uniform(2, 5))

        results_page = SearchResultsPage(driver)
        items = results_page.get_product_info_list()
        count = len(items)

        actual = f"수집된 상품 개수: {count}개"
        if count == 0:
            status = "PASS"
        else:
            status = "FAIL"
            actual += " (결과가 없어야 하는데 상품이 잡힘)"

    except Exception as e:
        status = "ERROR"
        actual = f"에러: {str(e)}"

    reporter.log_result(tc_id, module, scenario, keyword, expected, actual, status)


# =================================================================================
# 3. [Boundary Test] 최대 길이 입력 테스트 (TC 06)
# =================================================================================
def test_search_boundary_long_string(driver):
    """
    [TC_SEARCH_06] 엄청 긴 문자열 입력 시 크래시 여부 확인
    - 목적: 입력 필드 한계 테스트 (Boundary Testing)
    """
    tc_id = "TC_SEARCH_06"
    module = "Search"
    scenario = "최대 길이 문자열(a * 100자) 입력 테스트"
    keyword = "a" * 100
    expected = "에러 없이 검색 결과 페이지로 이동"

    try:
        main_page = AmazonMainPage(driver)
        main_page.open()

        main_page.search_product(keyword)
        time.sleep(random.uniform(2, 5))

        # 1. 검증 (Verify)
        # 상품 개수보다는, 에러 페이지 반환 여부 확인
        current_url = driver.current_url

        # Amazon 검색 URL --> 's?k=' 파라미터
        # https://www.amazon.co.jp/s?k=test@@
        if "s?k=" in current_url:
            status = "PASS"
            actual = "검색 결과 페이지로 정상 진입"
        else:
            status= "FAIL"
            actual = f"검색 페이지 진입 실패 (URL: {current_url})"

    except Exception as e:
        status = "ERROR"
        actual = f"브라우저 에러(Crash) 발생: {str(e)}"

    # 2. 리포트 저장
    reporter.log_result(tc_id, module, scenario, "a * 100 char", expected, actual, status)

















