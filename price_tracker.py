import csv
import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 🕒 현재 시간 (한국 시간)
now = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")
print("📂 현재 경로 파일 목록:", os.listdir())

# ✅ 가격 태그의 구체적 CSS 선택자
PRICE_SELECTOR = "td[valign='bottom'] font span"

# 상품명으로 안전한 파일명 만들기
def clean_filename(name):
    return "_".join(name.split()).replace("/", "_").replace("(", "").replace(")", "")

# ✅ Selenium으로 가격 수집
def fetch_price(url, driver):
    try:
        driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        price_tag = driver.find_element(By.CSS_SELECTOR, PRICE_SELECTOR)
        if price_tag:
            return price_tag.text.strip()
    except Exception as e:
        print(f"[에러] 가격 수집 실패: {e}")
    return None

# ✅ 전체 실행
def run_all():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 백그라운드 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    with open("items.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["상품명"].strip()
            url = row["URL"].strip()
            price = fetch_price(url, driver)

            if price:
                filename = f"price_log_{clean_filename(name)}.csv"
                with open(filename, "a", newline="", encoding="utf-8") as out:
                    writer = csv.writer(out)
                    writer.writerow([now, price])
                print(f"✅ {name}: {price} 저장됨 → {filename}")
            else:
                print(f"❌ {name}: 가격 수집 실패")

    driver.quit()

if __name__ == "__main__":
    run_all()
