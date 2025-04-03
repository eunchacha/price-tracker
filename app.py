from flask import Flask
import requests
from bs4 import BeautifulSoup
import os  # 여기로 옮기기!

app = Flask(__name__)

@app.route("/")
def price_check():
    url = "https://www.usedgt.co.kr/shop/goods/goods_view.php?goodsno=123456"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    price_tag = soup.select_one(".item_price")
    price = price_tag.get_text(strip=True) if price_tag else "가격을 찾을 수 없음"
    
    return f"""
    <h2>🎸 가격 추적 결과</h2>
    <p><strong>가격:</strong> {price}</p>
    """

# ✅ 이거 하나만 남기세요!
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
