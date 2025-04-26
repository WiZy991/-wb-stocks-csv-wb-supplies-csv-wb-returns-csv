from flask import Flask, jsonify, request, Response
import requests
import os
import csv
import io

app = Flask(__name__)

# Токены Wildberries API
WB_STATISTICS_TOKEN = os.getenv("WB_STATISTICS_TOKEN", "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MDU3OTM4NywiaWQiOiIwMTk2M2VkYy1lYjc4LTc5NGQtOTljOC04NTQ5YTE1NGI1NWEiLCJpaWQiOjI3ODY4NjAyLCJvaWQiOjEyMTA4ODYsInMiOjEwNzM3NDE4MjgsInNpZCI6IjgxOWMxZjQ2LTU0ODMtNDc0ZS05ZjM1LTlhZWUxNWM2MTQ1MyIsInQiOmZhbHNlLCJ1aWQiOjI3ODY4NjAyfQ.LEqGxxnyXzvQu3GCj6c_EeTaoZiCMIwm8f7vwf7w08MXE2HX-E9E_jguGxGXBa9W4hvcPQKlnap9xDlB0DqMHA")
WB_SUPPLIES_TOKEN = os.getenv("WB_SUPPLIES_TOKEN", "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MDU3OTQ2MSwiaWQiOiIwMTk2M2VkZS0wYzBjLTdiZWUtYWIwMS1mNzliOTY1MjE2ZjEiLCJpaWQiOjI3ODY4NjAyLCJvaWQiOjEyMTA4ODYsInMiOjEwNzM3NDI4NDgsInNpZCI6IjgxOWMxZjQ2LTU0ODMtNDc0ZS05ZjM1LTlhZWUxNWM2MTQ1MyIsInQiOmZhbHNlLCJ1aWQiOjI3ODY4NjAyfQ.PPoPMnPG3DwQPWS_AJ24V-GYGKkaUSl5IvIqCM3sY_qZJFKkLiAd8VziegotxmP17e5j-YTi1vgVMs_o_71YyQ")
WB_RETURNS_TOKEN = os.getenv("WB_RETURNS_TOKEN", "eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjUwMjE3djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTc2MDU3OTQyNywiaWQiOiIwMTk2M2VkZC04N2Q5LTcxN2MtYmU3Zi1iOGU5MWViM2Q1OTIiLCJpaWQiOjI3ODY4NjAyLCJvaWQiOjEyMTA4ODYsInMiOjEwNzM3NDM4NzIsInNpZCI6IjgxOWMxZjQ2LTU0ODMtNDc0ZS05ZjM1LTlhZWUxNWM2MTQ1MyIsInQiOmZhbHNlLCJ1aWQiOjI3ODY4NjAyfQ.d2xOjO99C0UL790mhz97hgKSiYBILC6raFukwINF8cxVitT5kmDB8yigkz1TLqJqpx76--tj7u3bZhWG7PCFvg")

@app.route('/')
def home():
    return "✅ WB Proxy API is working"

@app.route('/wb/sales-csv')
def get_sales_csv():
    date_from = request.args.get('dateFrom')
    if not date_from:
        return "dateFrom is required (format YYYY-MM-DD)", 400

    headers = {"Authorization": f"Bearer {WB_STATISTICS_TOKEN}"}
    url = f"https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={date_from}"
    try:
        response = requests.get(url, headers=headers)
        if not response.ok:
            return f"Error from WB: {response.text}", response.status_code

        data = response.json()
        if not data:
            return "No data available", 204

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        return Response(output.getvalue(), mimetype="text/csv")

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/wb/stocks-csv')
def get_stocks_csv():
    headers = {"Authorization": f"Bearer {WB_STATISTICS_TOKEN}"}
    url = "https://statistics-api.wildberries.ru/api/v1/supplier/stocks"
    try:
        response = requests.get(url, headers=headers)
        if not response.ok:
            return f"Error from WB: {response.text}", response.status_code

        data = response.json()
        if not data:
            return "No data available", 204

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        return Response(output.getvalue(), mimetype="text/csv")

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/wb/supplies-csv')
def get_supplies_csv():
    headers = {"Authorization": f"Bearer {WB_SUPPLIES_TOKEN}"}
    url = "https://suppliers-api.wildberries.ru/api/v2/supplies"
    try:
        response = requests.get(url, headers=headers)
        if not response.ok:
            return f"Error from WB: {response.text}", response.status_code

        data = response.json()
        if not data:
            return "No data available", 204

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        return Response(output.getvalue(), mimetype="text/csv")

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/wb/returns-csv')
def get_returns_csv():
    date_from = request.args.get('dateFrom')
    if not date_from:
        return "dateFrom is required (format YYYY-MM-DD)", 400

    headers = {"Authorization": f"Bearer {WB_STATISTICS_TOKEN}"}
    url = f"https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={date_from}"
    try:
        response = requests.get(url, headers=headers)
        if not response.ok:
            return f"Error from WB: {response.text}", response.status_code

        data = response.json()
        if not data:
            return "No data available", 204

        # Фильтрация возвратов
        returns_data = [item for item in data if item.get("orderType", "").lower() == "возврат"]

        if not returns_data:
            return "No returns found", 204

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=returns_data[0].keys())
        writer.writeheader()
        writer.writerows(returns_data)

        return Response(output.getvalue(), mimetype="text/csv")

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

