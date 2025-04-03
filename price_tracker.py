import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def get_price():
    url = "http://www.schoolmusic.co.kr/Shop/index.php3?var=Good&Good_no=64553&version=pc"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    price_tag = soup.select_one(".price_num")  # 정확한 selector는 이후 확인!
    if price_tag:
        price = price_tag.get_text(strip=True)
        return price
    else:
        return None

def save_price(price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("price_log.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([now, price])

# 수동 실행용
if __name__ == "__main__":
    price = get_price()
    if price:
        save_price(price)
        print(f"[{datetime.now()}] 가격 저장됨: {price}")
    else:
        print("❌ 가격을 찾을 수 없음")
