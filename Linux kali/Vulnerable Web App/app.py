from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    # ส่งไฟล์ index.html จากโฟลเดอร์ปัจจุบัน
    return send_from_directory('.', 'index.html')

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.json
    name = data.get('name', 'Guest')
    
    # จงใจให้มี XSS: เราส่งคืนชื่อไปในรูปแบบ HTML โดยไม่มีการตรวจสอบ
    return jsonify({
        "status": "success",
        "message": f"✨ <span class='user-name'>{name}</span> - Your profile is now active in the system!"
    })

if __name__ == '__main__':
    # รันที่พอร์ต 5000
    app.run(port=8888, debug=False)