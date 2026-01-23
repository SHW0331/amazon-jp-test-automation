import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_full_scenario_skip_sponsored():
    print(">>> [Step 1] 브라우저 실행")
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # =================================================================
        # 1. 배송지 변경 (Pages/AmazonMainPage 로직)
        # =================================================================
        print("\n>>> [Step 2] 배송지 변경 (한국 -> 도쿄) 시작")
        driver.get("https://www.amazon.co.jp")
        time.sleep(2)  # 로딩 대기

        # 1-1. 배송지 아이콘 클릭
        loc_icon = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "nav-global-location-popover-link"))
        )
        loc_icon.click()
        time.sleep(1)

        # 1-2. 우편번호 입력 (100-0001)
        # 앞자리
        zip1_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "GLUXZipUpdateInput_0"))
        )
        zip1_input.clear()
        zip1_input.send_keys("100")

        # 뒷자리
        zip2_input = driver.find_element(By.ID, "GLUXZipUpdateInput_1")
        zip2_input.clear()
        zip2_input.send_keys("0001")

        # 1-3. 확인 버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "#GLUXZipUpdate input").click()
        time.sleep(1)

        # 1-4. 완료 버튼 클릭 (팝업 닫기)
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.NAME, "glowDoneButton"))
            ).click()
        except:
            pass  # 이미 닫혔으면 패스

        # 1-5. 새로고침 후 확인
        time.sleep(2)
        driver.refresh()
        print("   -> 배송지 변경 완료! ✅")

        # =================================================================
        # 2. 키워드 검색 (Pages/AmazonMainPage 로직)
        # =================================================================
        keyword = "Nintendo Switch"
        print(f"\n>>> [Step 3] 키워드 검색: '{keyword}'")

        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "twotabsearchtextbox"))
        )
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        print("   -> 검색어 입력 및 엔터 완료")

        # =================================================================
        # 3. 스폰서 제외하고 클릭 (Pages/SearchResultsPage 로직)
        # =================================================================
        print("\n>>> [Step 4] 스폰서(광고) 제외하고 첫 번째 상품 클릭")

        # Locator 정의 (해원님이 찾으신 것들)
        card_locator = (By.CSS_SELECTOR, "div[data-cy='asin-faceout-container']")
        sponsored_locator = (By.CSS_SELECTOR, "span.puis-label-popover-default")
        title_link_locator = (By.CSS_SELECTOR, "div[data-cy='title-recipe'] a")
        title_text_locator = (By.CSS_SELECTOR, "div[data-cy='title-recipe'] a h2 span")

        # 카드 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(card_locator)
        )
        cards = driver.find_elements(*card_locator)
        print(f"   -> 검색된 총 카드 수: {len(cards)}개")

        found_organic = False

        for index, card in enumerate(cards):
            try:
                # 3-1. 광고 여부 확인
                if len(card.find_elements(*sponsored_locator)) > 0:
                    print(f"     [Skip] {index + 1}번째 상품은 '광고(Sponsored)' 입니다. 패스!")
                    continue

                # 3-2. 진짜 상품 발견 및 클릭
                title_text = card.find_element(*title_text_locator).text
                print(f"     [Found] {index + 1}번째 상품이 '진짜(Organic)' 입니다!")
                print(f"     -> 제목: {title_text[:40]}...")

                link = card.find_element(*title_link_locator)
                link.click()
                found_organic = True

                print("   -> 클릭 완료! 상세 페이지로 이동 🚀")
                break  # 루프 종료

            except Exception as e:
                print(f"     [Warning] 카드 처리 중 에러: {e}")
                continue

        if not found_organic:
            print("   -> ⚠️ 광고 아닌 상품을 찾지 못했습니다.")
            return

        # =================================================================
        # 4. (중요) 탭 전환 확인
        # =================================================================
        time.sleep(3)  # 새 탭 열릴 시간 대기
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            print(f"\n>>> [Step 5] 새 탭으로 포커스 이동 완료! (현재 제목: {driver.title[:10]}...)")
        else:
            print(f"\n>>> [Step 5] 같은 탭에서 열림 (현재 제목: {driver.title[:10]}...)")

    except Exception as e:
        print(f"\n>>> ☠️ 에러 발생: {e}")

    finally:
        input("\n>>> [Test End] 엔터를 누르면 브라우저를 닫습니다...")
        driver.quit()


if __name__ == "__main__":
    test_full_scenario_skip_sponsored()