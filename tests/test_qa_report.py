import pytest
import openpyxl
import os
import time
from datetime import datetime
from selenium import webdriver
from pages.amazon_main_page import AmazonMainPage
from pages.search_results_page import SearchResultsPage

def test_generate_qa_report():
    """
    [QA Report] 자동화 테스트 수행 후 결과 리포트(Excel) 생성
    시나리오:
    1. 정상 검색 테스트
    2. 페이지 이동 테스트
    3. 결과 없음 테스트
    :return:
    """