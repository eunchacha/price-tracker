import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

print("📂 현재 경로 파일 목록:", os.listdir())

# ✅ 가격 태그 선택자
PRICE_SELECTOR = "td[valign='bottom'] font > span.price"

# ✅ 상품명에 따라 파일 이름을 안전하게 만들기
def clean_filename(name):
    return "_".join(name.split()).replace("/", "_").replace("(", "").replace(")", "")

# ✅ 가격 수집 함수
def fetch_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.select_one(PRICE_SELECTOR)
        if price_tag:
            # 숫자만 추출 (ex. ₩456,000 → 456000)
            price = ''.join(filter(str.isdigit, price_tag.get_text()))
            return price
    except Exception as e:
        print("[에러] 가격 수집 실패:", e)
    return None

# ✅ items.csv 읽고 각 상품별 가격 수집 후 개별 CSV 저장
def run_all():
    now = (datetime.utcnow() + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")

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

if __name__ == "__main__":
    run_all()
