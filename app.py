from flask import Flask, send_file, render_template_string
import threading
import time
import subprocess
import os

app = Flask(__name__)

# ✅ HTML 페이지 구성
@app.route("/")
def index():
    html = """
    <html>
        <head>
            <title>🎸 가격 추적</title>
        </head>
        <body style="text-align:center; font-family:sans-serif;">
            <h2>🎸 SchoolMusic 데임 Dame PS-5 베이스기타 (TS) 가격 변동 그래프</h2>
            <img src="/graph" style="width:80%;">
        </body>
    </html>
    """
    return render_template_string(html)

# ✅ 그래프 이미지 반환
@app.route("/graph")
def graph():
    return send_file("static/price_graph.png", mimetype="image/png")

# ✅ 백그라운드에서 price_tracker.py를 10분마다 실행하는 함수
def run_price_tracker_every_10min():
    while True:
        print("⏱ price_tracker.py 실행 중...")
        subprocess.run(["python", "price_tracker.py"])
        time.sleep(600)  # 600초 = 10분

# ✅ 앱 시작 시 자동 실행
if __name__ == "__main__":
    # Railway용 포트 설정
    port = int(os.environ.get("PORT", 5000))

    # 🌀 자동 수집 쓰레드 시작
    threading.Thread(target=run_price_tracker_every_10min, daemon=True).start()

    # 🌐 Flask 웹 서버 실행
    app.run(host="0.0.0.0", port=port)
