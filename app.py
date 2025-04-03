from flask import Flask, render_template_string
import csv
from collections import defaultdict

app = Flask(__name__)

@app.route("/")
def index():
    data = defaultdict(dict)
    hours = set()

    with open("price_log.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            timestamp, price = row
            date, time = timestamp.split(" ")
            hour = time[:2] + ":00"
            data[date][hour] = price
            hours.add(hour)

    sorted_hours = sorted(hours)

    html = """
    <html>
    <head>
        <title>🎸 가격 추적 테이블</title>
        <style>
            body { font-family: sans-serif; text-align: center; }
            table { margin: auto; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 6px 12px; }
            th { background-color: #f0f0f0; }
            .changed { background-color: yellow; padding: 2px; }
        </style>
    </head>
    <body>
        <h2>🎸 날짜별 시간대 가격 추적</h2>
        <table>
            <tr>
                <th>날짜</th>
                {% for hour in hours %}
                    <th>{{ hour }}</th>
                {% endfor %}
            </tr>
            {% for date, row in data.items() %}
                <tr>
                    <td>{{ date }}</td>
                    {% set prev_price = None %}
                    {% for hour in hours %}
                        {% set current = row.get(hour, "") %}
                        {% if prev_price and current and current != prev_price %}
                            <td><span class="changed">{{ current }}</span></td>
                        {% else %}
                            <td>{{ current }}</td>
                        {% endif %}
                        {% set prev_price = current %}
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html, data=dict(data), hours=sorted_hours)

# ✅ Railway용 서버 실행 코드
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
