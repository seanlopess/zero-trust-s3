from flask import Flask, jsonify, request, render_template
import boto3
import pymysql
import os
from datetime import datetime

app = Flask(__name__)

# Initialize S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'zero-trust-storage-bucket'  # Replace with your actual bucket name

# Database configuration from environment variables
RDS_HOST = os.getenv("RDS_HOST", "zerotrustdb.chqsoog2ufaq.ap-south-1.rds.amazonaws.com")
RDS_USER = os.getenv("RDS_USER", "admin")
RDS_PASSWORD = os.getenv("RDS_PASSWORD", "Seanne#13")
RDS_DB = os.getenv("RDS_DB", "zerotrustdb")

# Function to get the current database time
def get_db_time():
    try:
        conn = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        with conn.cursor() as cur:
            cur.execute("SELECT NOW() AS now;")
            row = cur.fetchone()
        conn.close()
        return row["now"] if row else None
    except Exception as e:
        return f"ERROR: {e}"

# Helper function to get timestamp
def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Upload file to S3
def upload_file(file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    try:
        s3.upload_file(file_name, BUCKET_NAME, object_name)
    except Exception as e:
        return str(e)
    return None

# Download file from S3
def download_file(object_name, file_name):
    try:
        s3.download_file(BUCKET_NAME, object_name, file_name)
    except Exception as e:
        return str(e)
    return None

# Root endpoint
@app.route('/ui', methods=['GET'])
def hello():
    now = get_db_time()
    return jsonify({
        "message": "Hello, Zero Trust Architecture!",
        "db_time": str(now),
        "timestamp": get_current_timestamp()
    })

# File upload endpoint
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({
            "error": "No file provided",
            "timestamp": get_current_timestamp()
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "error": "Empty filename",
            "timestamp": get_current_timestamp()
        }), 400

    # Save locally and upload
    file.save(file.filename)
    error = upload_file(file.filename)
    if error:
        return jsonify({
            "error": error,
            "timestamp": get_current_timestamp()
        }), 500

    return jsonify({
        "message": f"File {file.filename} uploaded successfully",
        "timestamp": get_current_timestamp()
    }), 200

# File download endpoint
@app.route('/download/<path:key>', methods=['GET'])
def download(key):
    file_name = f"downloaded_{key}"
    error = download_file(key, file_name)

    if error:
        return jsonify({
            "error": error,
            "timestamp": get_current_timestamp()
        }), 500

    return jsonify({
        "message": f"File {key} downloaded successfully!",
        "timestamp": get_current_timestamp()
    }), 200

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

