import csv
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

print("📂 현재 경로 파일 목록:", os.listdir())

# ✅ 상품명을 안전한 파일명으로 변환
def clean_filename(name):
    return "_".join(name.split()).replace("/", "_").replace("(", "").replace(")", "")

# ✅ 가격 수집 함수 (스타일 기반 정확 추출)
def fetch_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        td = soup.find("td", valign="bottom")
        if not td:
            print("❌ td[valign='bottom'] 요소 없음")
            return None

        fonts = td.find_all("font")
        for font in fonts:
            style = font.get("style", "")
            if "font-size:30px" in style and "font-weight:bold" in style:
                span = font.find("span")
                if span:
                    price = ''.join(filter(str.isdigit, span.get_text()))
                    return price

        print("❌ 조건에 맞는 가격 정보 없음")
    except Exception as e:
        print(f"[에러] 가격 수집 실패: {e}")
    return None

# ✅ items.csv 읽고 상품별 가격 수집 후 로그 저장
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

if __name__ == "__main__":
    run_all()
