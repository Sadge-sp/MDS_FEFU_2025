
from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from dotenv import load_dotenv
import boto3
import os
import redis

app = Flask(__name__)
load_dotenv()


# PostgreSQL setup
engine = create_engine(os.getenv('DATABASE_URL'))
# Redis setup (placeholder)
redis_client = redis.from_url(os.getenv('REDIS_URL'))
# MinIO setup
s3_client = boto3.client('s3',
                        endpoint_url=os.getenv('S3_ENDPOINT_URL'),
                        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
                        aws_secret_access_key=os.getenv('S3_SECRET_KEY'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    s3_client.upload_fileobj(file, os.getenv('S3_BUCKET'), file.filename)
    return jsonify({'message': f'File {file.filename} uploaded to {os.getenv("S3_BUCKET")}'}), 200

@app.route('/test_db', methods=['GET'])
def test_db():
    with engine.connect() as connection:
        return jsonify({'message': 'Connected to PostgreSQL!'}), 200

@app.route('/test_redis', methods=['GET'])
def test_redis():
    redis_client.set('test_key', 'test_value')
    value = redis_client.get('test_key').decode('utf-8')
    return jsonify({'message': f'Redis value: {value}'}), 200

@app.route('/')
def home():
    return render_template('homepage.html')

# Страница входа
@app.route('/login')
def login():
    return render_template('login.html')

# Страница создания аккаунта
@app.route('/register')
def register():
    return render_template('creatacc.html')

# Страница конструктора
@app.route('/configurator')
def configurator():
    return render_template('buildpage.html')

# Страница корзины
@app.route('/cart')
def cart():
    return render_template('card.html')

# Страница доставки
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

# Страница отслеживания заказа
@app.route('/track')
def track():
    return render_template('ordertsking.html')

# Страница поддержки
@app.route('/support')
def support():
    return render_template('suport.html')

# Страница профиля мыши
@app.route('/mouse_profile')
def mouse_profile():
    return render_template('mouse_profile.html')

# Страница фильтра мышей
@app.route('/catalog')
def catalog():
    return render_template('filter_mouse.html')





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

