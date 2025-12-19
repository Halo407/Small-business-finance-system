from flask import Flask, request, jsonify, send_from_directory
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')

# In-memory storage (ganti dengan database di produksi)
transactions = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data or 'type' not in data or 'amount' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    transaction = {
        'id': len(transactions) + 1,
        'type': data['type'],  # 'income' atau 'expense'
        'amount': float(data['amount']),
        'description': data['description'],
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
    }
    transactions.append(transaction)
    return jsonify(transaction), 201

@app.route('/api/summary', methods=['GET'])
def get_summary():
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    net_profit = total_income - total_expense
    return jsonify({
        'total_income': round(total_income, 2),
        'total_expense': round(total_expense, 2),
        'net_profit': round(net_profit, 2)
    })

@app.route('/api/monthly', methods=['GET'])
def monthly_report():
    report = {}
    for t in transactions:
        month = t['date'][:7]  # format: YYYY-MM
        if month not in report:
            report[month] = {'income': 0, 'expense': 0}
        if t['type'] == 'income':
            report[month]['income'] += t['amount']
        else:
            report[month]['expense'] += t['amount']
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)
