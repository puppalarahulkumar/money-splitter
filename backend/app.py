from flask import Flask,request,jsonify
from flask_cors import CORS
import pytesseract
import cv2
from werkzeug.utils import secure_filename
import re
import math

import os
app=Flask(__name__)
CORS(app)

UPLOAD_FOLDER='uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

def extract_text(image_path):
    image=cv2.imread(image_path)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    text=pytesseract.image_to_string(gray)
    return text

@app.route('/upload',methods=['post'])
def upload_file():
    if 'image' not in request.files:
        return 'No image uploaded',400
    
    file=request.files['image']
    
    if file.filename=='':
        return 'No selected file',400
    if file:
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return jsonify({"message": "File uploaded successfully!", "filename": filename}), 200
    else:
        return jsonify({"message": "No file provided"}), 400
@app.route('/process',methods=['post'])
def process_image():
    filename=request.json.get('filename')

    if filename:
        image_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        print(image_path)
        if os.path.exists(image_path):
            print("the image path exists")
            text=extract_text(image_path)
            amount=re.findall(r'(\d+)(?=/\-)',text)
            print(amount)
            amount=list(map(int,amount))
            total_amount=sum(amount)
            return jsonify({'text':total_amount}),200

        else:
            print('error somewhere')
            return jsonify({'message':"file not found"}),400
    else:
        return jsonify({'message':'filename not provided'}),400

if __name__=='__main__':
    app.run(debug=True)
