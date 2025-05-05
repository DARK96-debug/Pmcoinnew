from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import random
import time

app = Flask(__name__)

# Ma'lumotlar bazasi (bu misolda faqat xotiraga saqlash)
users_db = {}
missions_db = {}
referrals_db = {}

# Admin uchun login
admin_credentials = {
    "admin@user.com": generate_password_hash("admin123")
}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']

    if username in users_db:
        return jsonify({"success": False, "message": "Foydalanuvchi allaqachon mavjud!"})

    hashed_password = generate_password_hash(password)
    users_db[username] = {'password': hashed_password, 'balance': 0.000001, 'referals': []}
    return jsonify({"success": True, "message": "Foydalanuvchi ro'yxatdan o'tdi!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    if username not in users_db or not check_password_hash(users_db[username]['password'], password):
        return jsonify({"success": False, "message": "Noto'g'ri foydalanuvchi nomi yoki parol!"})

    return jsonify({"success": True, "message": "Kirish muvaffaqiyatli!"})

@app.route('/referral', methods=['POST'])
def referral():
    data = request.json
    referrer = data['referrer']
    referree = data['referree']

    if referrer not in users_db:
        return jsonify({"success": False, "message": "Foydalanuvchi mavjud emas!"})

    users_db[referrer]['balance'] += 0.000003
    referrals_db[referree] = referrer
    return jsonify({"success": True, "message": "Referal muvaffaqiyatli amalga oshirildi!"})

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender = data['sender']
    receiver = data['receiver']
    amount = data['amount']

    if sender not in users_db or receiver not in users_db:
        return jsonify({"success": False, "message": "Foydalanuvchilar topilmadi!"})

    sender_balance = users_db[sender]['balance']
    if sender_balance < amount:
        return jsonify({"success": False, "message": "Yetarlicha balans mavjud emas!"})

    users_db[sender]['balance'] -= amount
    users_db[receiver]['balance'] += amount

    # 5% komissiya
    commission = amount * 0.05
    users_db['admin']['balance'] += commission

    return jsonify({"success": True, "message": f"{amount} PM coin otkazildi."})

if __name__ == '__main__':
    app.run(debug=True)
