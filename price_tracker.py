import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

print("📂 현재 경로 파일 목록:", os.listdir())

# 가격 태그 선택자
PRICE_SELECTOR = "td[valign='bottom'] font > span"

# 상품명에 따라 안전한 파일명 만들기
def clean_filename(name):
    return "_".join(name.split()).replace("/", "_").replace("(", "").replace(")", "")

# 가격 수집 함수 (헤더 강화)
def fetch_price(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.schoolmusic.co.kr",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()  # 403 등 예외 발생시 catch
        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.select_one(PRICE_SELECTOR)
        if price_tag:
            return price_tag.get_text(strip=True)
        else:
            print("[에러] 가격 태그를 찾지 못함")
    except Exception as e:
        print(f"[에러] 가격 수집 실패: {e}")
    return None

# 전체 실행 로직
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
