from flask import Flask, send_file, render_template_string
import os  # ← 이거 꼭 필요!

app = Flask(__name__)

@app.route("/")
def index():
    html = """
    <html>
        <head>
            <title>🎸 가격 추적</title>
        </head>
        <body style="text-align:center; font-family:sans-serif;">
            <h2>🎸 SchoolMusic (데임 Dame PS-5 베이스기타 (TS))가격 변동 그래프</h2>
            <img src="/graph" style="width:80%;">
        </body>
    </html>
    """
    return render_template_string(html)

@app.route("/graph")
def graph():
    return send_file("static/price_graph.png", mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 환경변수에서 포트 가져오기
    app.run(host="0.0.0.0", port=port)
