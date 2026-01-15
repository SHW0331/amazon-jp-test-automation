import pytest
import os
import time
import random
import openpyxl
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

        search_keyword = "nintndo switch"
        amazon_main.search_product(search_keyword)

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
        driver.quit()

def test_amazon_search_and_save_excel():
    """검색 후, 결과를 엑셀  파일로 저장하는 테스트"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    output_dir = "outputs"

    try:
        amazon_main = AmazonMainPage(driver)
        amazon_main.open()

        search_keyword = "nintndo switch"
        amazon_main.search_product(search_keyword)

        # 1. 결과 리스트 가져오기
        results_page = SearchResultsPage(driver)
        products = results_page.get_product_info_list()

        # 2. 엑셀 Workbook()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Amazon Results"
        ws.append(["No.", "Product Title", "Price", "Keyword"]) # 헤더 작성

        # 3. 리스트에 있는 내용을 하나씩 꺼내서 엑셀에 작성
        for i, item in enumerate(products, 1):
            ws.append([i, item['title'], item['price'], search_keyword])

        # 4. 파일로 저장
        file_name = "amazon_result_with_price.xlsx"
        save_path = os.path.join(output_dir, file_name)
        wb.save(save_path)

        # 5. 검증 : 리스트가 비어있지 않은지
        print(f"\n[PASS] Successfully saved {len(products)} items to '{file_name}'.")
        assert len(products) > 0, "Product list is empty!"

    finally:
        driver.quit()

def test_search_multiple_keywords():
    """여러 개의 키워드를 연속으로 검색하고 하나의 엑셀에 저장"""

    driver = webdriver.Chrome()
    driver.maximize_window()
    output_dir = "outputs"

    # 검색 키워드 설정
    search_keywords = [
        "マリオカート8 デラックス",
        "あつまれ どうぶつの森",
        "大乱闘スマッシュブラザーズ SPECIAL",
        "ゼルダの伝説 ブレス オブ ザ ワイルド",
        "スーパーマリオ オデッセイ",
    ]

    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Multi Search Results"
        ws.append(["No.", "Keyword", "Product Title", "Price"])

        total_count = 0

        for keyword in search_keywords:
            print(f"\n[INFO] Preparing to search for '{keyword}'... (Waiting for safety)")

            # Anti-Bot Wait (Random)
            time.sleep(random.uniform(2, 5))

            amazon_main = AmazonMainPage(driver)
            amazon_main.open()

            amazon_main.search_product(keyword)
            time.sleep(random.uniform(2, 5))

            result_page = SearchResultsPage(driver)
            products = result_page.get_product_info_list()

            for item in products:
                total_count += 1
                ws.append([total_count, keyword, item['title'], item['price']])

            print(f"-> Found {len(products)} items for '{keyword}'.")

        file_name = "amazon_multi_results.xlsx"
        save_path = os.path.join(output_dir, file_name)
        wb.save(save_path)

        print(f"\n[PASS] Successfully saved {total_count} items to '{file_name}'.")

        # 검증 : total count가 0인지
        assert total_count > 0, "No Products found for any keyword!"

    finally:
        driver.quit()



