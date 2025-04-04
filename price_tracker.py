import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

print("📂 현재 경로 파일 목록:", os.listdir())

# 가격 태그 선택자
PRICE_SELECTOR = "td[valign='bottom'] font > span"

# 파일 이름에 사용할 수 있게 상품명 정리
def clean_filename(name):
    return "_".join(name.split()).replace("/", "_").replace("(", "").replace(")", "")

# 가격 수집 함수
def fetch_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.schoolmusic.co.kr/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 403:
            print(f"[에러] 가격 수집 실패: 403 Forbidden for url: {url}")
            return None
        elif res.status_code != 200:
            print(f"[에러] 가격 수집 실패: 상태 코드 {res.status_code} for url: {url}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.select_one(PRICE_SELECTOR)

        if price_tag:
            return price_tag.get_text(strip=True)

    except Exception as e:
        print("[에러] 가격 수집 실패:", e)
    
    return None

# 전체 수집 실행 함수
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
