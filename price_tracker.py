import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# ✅ 가격 크롤링 함수
def get_price():
    url = "http://www.schoolmusic.co.kr/Shop/index.php3?var=Good&Good_no=64553&version=pc"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 💡 정확한 selector
    price_tag = soup.select_one("td[valign='bottom'] font > span")
    if price_tag:
        price = price_tag.get_text(strip=True)
        return price
    else:
        return None

# ✅ 가격 저장 함수 (CSV)
def save_price(price):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("price_log.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([now, price])

# ✅ 가격 변동 그래프 생성 함수
def generate_graph():
    times = []
    prices = []

    try:
        with open("price_log.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    time_str = row[0]
                    price_str = row[1]
                    if not price_str.strip():
                        continue
                    times.append(datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S"))
                    prices.append(int(price_str.replace(",", "").strip()))
                except:
                    continue
    except FileNotFoundError:
        print("⚠️ price_log.csv 파일이 없습니다.")
        return

    if not prices:
        print("⚠️ 유효한 가격 데이터가 없어 그래프를 그릴 수 없습니다.")
        return

    os.makedirs("static", exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(times, prices, marker="o", linestyle="-", color="blue")

    # ✅ 가격 숫자 표시
    for t, p in zip(times, prices):
        plt.text(t, p, f"{p:,}", ha='center', va='bottom', fontsize=9, color='black')

    plt.title("🎸 SchoolMusic 가격 변동 그래프")
    plt.xlabel("시간")
    plt.ylabel("가격 (원)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig("static/price_graph.png")
    print("✅ 그래프가 static/price_graph.png 에 저장되었습니다.")

# ✅ 메인 실행
if __name__ == "__main__":
    price = get_price()
    if price:
        save_price(price)
        print(f"[{datetime.now()}] 가격 저장됨: {price}")
        generate_graph()
    else:
        print("❌ 가격을 찾을 수 없음")
