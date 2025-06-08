
from flask import Flask, request, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)

