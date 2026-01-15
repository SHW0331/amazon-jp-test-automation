# 🛒 Amazon Japan Test Automation Project

## 1. 파일별 주요 역할 및 개발 내역 (File History) - 26.01.14

- **`pages/amazon_main_page.py`**
  - 아마존 메인 URL 접속, 검색창 및 버튼 요소(Locator) 관리, 검색 동작 메서드 구현.

- **`pages/search_results_page.py`**
  - 검색 결과 페이지의 CSS Selector 정의, 광고 제외 및 텍스트 공백 제거를 포함한 상품명 리스트 추출 기능.

- **`tests/test_search.py`**
  - 실제 테스트 시나리오 실행 파일. `WebDriverWait`로 동기화 문제 해결, `openpyxl`을 이용한 엑셀 저장 로직 통합, `driver.quit()`으로 종료 처리.

- **`.gitignore`**
  - 깃허브 업로드 제외 설정 (`venv`, `__pycache__`, `*.xlsx` 등 불필요한 파일 차단).

- **`amazon_result.xlsx`**
  - 자동화 테스트 실행 후 생성되는 결과 파일 (순위, 상품명, 검색어 저장).

## 2. 파일별 주요 역할 및 개발 내역 (File History) - 26.01.15

- **`pages/search_results_page.py`**
  - 상품 카드(Card) 하나를 잡고, 그 안에서 제목과 가격을 추출하는 구조로 변경.

- **`tests/test_search.py`**
  - 딕셔너리 형태(`{'title': '...', 'price': '...'}`)의 데이터를 처리하도록 수정.
  - 엑셀 헤더에 **'Price'** 열 추가.

- **테스트 코드 로직 확장 (`tests/test_search.py`)**
  - 기존: "nintendo switch"라는 고정된 단어 하나만 검색.
  - 변경: `["PS5", "AirPods", "Keyboard"]` 처럼 리스트에 있는 모든 검색어를 순서대로 실행.


- **문제점 : 스폰서 상품 예외처리 필요**
  - スポンサー情報を表示、または広告フィードバックを残す
  - span[class="puis-label-popover-default"]

## 프로젝트 구조 (Folder Structure)
```text
amazon-jp-test-automation/
├── pages/                  # [POM] 페이지별 동작과 요소를 관리하는 폴더
│   ├── __init__.py
│   ├── amazon_main_page.py # 메인 페이지 (검색창, 이동 등)
│   └── search_results_page.py # 검색 결과 페이지 (리스트 추출 등)
├── tests/                  # 실제 테스트 시나리오가 있는 폴더
│   ├── __init__.py
│   └── test_search.py      # 검색 및 엑셀 저장 테스트 코드
├── .gitignore              # 깃허브에 올리지 않을 파일 목록
└── amazon_result.xlsx      # (자동생성) 결과 엑셀 파일