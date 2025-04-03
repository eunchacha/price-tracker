from flask import Flask, render_template_string
import csv
import os
from collections import defaultdict

app = Flask(__name__)

# 상품별 가격 로그를 읽어서 딕셔너리로 반환
def load_price_logs():
    tables = {}
    for filename in os.listdir("."):
        if filename.startswith("price_log_") and filename.endswith(".csv"):
            product = filename[len("price_log_"):-len(".csv")].replace("_", " ")
            data = defaultdict(dict)
            hours = set()

            with open(filename, encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 2:
                        continue
                    timestamp, price = row
                    date, time = timestamp.split(" ")
                    hour = time[:2] + ":00"
                    data[date][hour] = price
                    hours.add(hour)

            tables[product] = {
                "data": dict(data),
                "hours": sorted(hours)
            }
    return tables

@app.route("/")
def index():
    all_tables = load_price_logs()

    html = """
    <html>
    <head>
        <title>🎸 가격 추적 테이블</title>
        <style>
            body { font-family: sans-serif; text-align: center; }
            table { margin: 20px auto; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 6px 12px; }
            th { background-color: #f0f0f0; }
            .changed { background-color: yellow; padding: 2px; }
        </style>
    </head>
    <body>
        <h1>🎸 여러 상품 가격 추적</h1>
        {% for name, table in tables.items() %}
            <h2>{{ name }}</h2>
            <table>
                <tr>
                    <th>날짜</th>
                    {% for hour in table.hours %}
                        <th>{{ hour }}</th>
                    {% endfor %}
                </tr>
                {% for date, row in table.data.items() %}
                    <tr>
                        <td>{{ date }}</td>
                        {% set prev_price = None %}
                        {% for hour in table.hours %}
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
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, tables=all_tables)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
