import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 현재 경로 출력 (디버깅용)
print("📂 현재 경로 파일 목록:", os.listdir())

# ✅ 가격 태그 선택자 (수정됨)
PRICE_SELECTOR = "td[valign='bottom'] span"

# ✅ 상품명을 안전한 파일명으로 변환
def clean_filename(name):
    return "_".join(name.split()).replace("/", "_").replace("(", "").replace(")", "")

# ✅ 가격 수집 함수
def fetch_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.select_one(PRICE_SELECTOR)
        if price_tag:
            text = price_tag.get_text(strip=True)
            price = ''.join(filter(str.isdigit, text))  # 숫자만 추출 (예: 456000)
            return price
    except Exception as e:
        print("[에러] 가격 수집 실패:", e)
    return None

# ✅ 전체 상품에 대해 가격 수집 및 로그 저장
def run_all():
    now = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")  # 한국 시간

    with open("items.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["상품명"].strip()
            url = row["URL"].strip()
            price = fetch_price(url)

            if price:
                filename = f"price_log_{clean_filename(name)}.csv"
                with open(filename, "a", newline="", encoding="utf-8") as out:
                    writer = csv.writer(out)
                    writer.writerow([now, price])
                print(f"✅ {name}: {price} 저장됨 → {filename}")
            else:
                print(f"❌ {name}: 가격 수집 실패")

# ✅ 직접 실행 시 호출
if __name__ == "__main__":
    run_all()
