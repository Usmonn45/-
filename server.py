from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Путь к JSON-файлу
DATA_FILE = "users.json"

# Создаём файл, если его нет
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# Загрузка всех пользователей
def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Сохранение всех пользователей
def save_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Создание или обновление пользователя ---
@app.route('/api/user', methods=['POST'])
def create_or_update_user():
    data = request.get_json()
    user_id = str(data.get('user_id'))
    username = data.get('username')
    ref = data.get('ref')

    users = load_users()

    if user_id not in users:
        users[user_id] = {
            'user_id': int(user_id),
            'username': username or 'Игрок',
            'balance': 0,
            'stars': 0,
            'level': 1,
            'referrals': 0,
            'friends': [],
            'dailyBonus': {'lastClaim': None, 'streak': 0},
            'tasks': {'subscribe': False, 'subscribe2': False, 'spins': 0, 'referrals': 0}
        }
    else:
        users[user_id]['username'] = username or users[user_id]['username']

    save_users(users)
    return jsonify(users[user_id])

# --- Получение пользователя ---
@app.route('/api/user', methods=['GET'])
def get_user():
    user_id = str(request.args.get('user_id'))
    users = load_users()

    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(users[user_id])

# --- Обновление пользователя ---
@app.route('/api/update', methods=['POST'])
def update_user():
    data = request.get_json()
    user_id = str(data.pop('id', None))
    if not user_id:
        return jsonify({'error': 'id is required'}), 400

    users = load_users()
    if user_id in users:
        users[user_id].update(data)
        save_users(users)
    return jsonify({'status': 'ok'})

# --- Главная страница ---
@app.route('/')
def home():
    return "MineStars API (JSON) is running 🚀"

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
