import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.amazon_main_page import AmazonMainPage
from pages.search_results_page import SearchResultsPage

# 1번 테스트 : 검색 후 제목 확인
def test_amazon_search():
    """ keyword search 정상적으로 작동하는지 확인하는 테스트 """

    # 1. 브라우저 옵션 설정 및 드라이버 실행
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # 2. 페이지 객체 생성 및 접속
        amazon_main = AmazonMainPage(driver)

        # 3. Amazon Page 접속 테스트 시나리오
        amazon_main.open()

        search_keyword = "nintendo switch"
        amazon_main.search_product(search_keyword)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.title_contains(search_keyword))

        # 4. Assertion: 결과 페이지 제목에 검색어가 포함되어 있는가?
        assert search_keyword in driver.title
        print(f"\n[PASS] Search test for '{search_keyword}' was successful!")

    finally:
        # 5. 브라우저 종료
        driver.quit()

# 2번 테스트 : 검색 결과 리스트 추출
def test_amazon_search_results_list():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        amazon_main = AmazonMainPage(driver)
        amazon_main.open()

        keyword = "nintndo switch"
        amazon_main.search_product(keyword)

        # 1. 결과 페이지에서 리스트 가져오기
        results_page = SearchResultsPage(driver)
        all_titles = results_page.get_all_product_titles()

        # 2. 결과 확인
        print(f"\n[INFO] Total items found: {len(all_titles)}")

        for i, title in enumerate(all_titles[:5], 1): # 상위 5개만 확인
            print(f"[ITEM {i}] {title}")

        assert len(all_titles) > 0
        print("\n[PASS] Product list extraction successful!")

    finally:
        driver.close()



