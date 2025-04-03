from flask import Flask, send_file, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    # HTML을 문자열로 직접 작성해 간단히 보여줍니다
    html = """
    <html>
        <head>
            <title>🎸 가격 추적</title>
        </head>
        <body style="text-align:center; font-family:sans-serif;">
            <h2>🎸 SchoolMusic 가격 변동 그래프</h2>
            <img src="/graph" style="width:80%;">
        </body>
    </html>
    """
    return render_template_string(html)

@app.route("/graph")
def graph():
    return send_file("static/price_graph.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
