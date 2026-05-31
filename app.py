from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

# Connect to AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('BUCKET_NAME')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        try:
            # This line uploads file to S3
            s3_client.upload_fileobj(file, BUCKET_NAME, file.filename)
            flash(f'Success! File "{file.filename}" uploaded to S3')
        except Exception as e:
            flash(f'Error: {str(e)}')
        
        return redirect(url_for('upload'))
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)