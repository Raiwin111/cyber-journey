from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from functools import wraps
import json
import os
from datetime import timedelta
import logging
import sys

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
# สั่งให้บันทึกลงไฟล์ชื่อ access.log
# ลบของเก่าออกแล้วแทนที่ด้วยอันนี้ครับ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("access.log"), # บันทึกลงไฟล์
        logging.StreamHandler()            # แสดงบนหน้าจอ Terminal
    ]
)
app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# ไฟล์เก็บข้อมูลสินค้า
PRODUCTS_FILE = 'products.json'

# ข้อมูลผู้ใช้ (username, password)
USERS = {
    'user': 'user123',
    'admin': 'admin123'
}

def load_products():
    """โหลดข้อมูลสินค้าจากไฟล์"""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return get_default_products()

def get_default_products():
    """ข้อมูลสินค้าเริ่มต้น: 3 สินค้า ราคาละ 5 ชิ้น"""
    return [
        {
            'id': 1,
            'name': 'Laptop Computer',
            'price': 25000,
            'quantity': 5,
            'description': 'High performance laptop'
        },
        {
            'id': 2,
            'name': 'Wireless Mouse',
            'price': 500,
            'quantity': 5,
            'description': 'Ergonomic wireless mouse'
        },
        {
            'id': 3,
            'name': 'USB-C Cable',
            'price': 300,
            'quantity': 5,
            'description': 'Fast charging USB-C cable'
        }
    ]

def save_products(products):
    """บันทึกข้อมูลสินค้าลงไฟล์"""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def login_required(f):
    """Decorator เพื่อตรวจสอบการเข้าสู่ระบบ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator เพื่อตรวจสอบสิทธิ์ admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_id') != 'admin':
            return jsonify({'status': 'error', 'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ===== Pages =====

@app.route('/')
def index():
    """หน้าแรก - ถ้าเข้าสู่ระบบแล้วให้ไปหน้าสินค้า"""
    if 'user_id' in session:
        return send_from_directory('.', 'products.html')
    return send_from_directory('.', 'index.html')

@app.route('/products')
def products_page():
    """หน้าสินค้า"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return send_from_directory('.', 'products.html')

@app.route('/admin')
def admin_page():
    """หน้า admin"""
    if 'user_id' not in session or session.get('user_id') != 'admin':
        return redirect(url_for('index'))
    return send_from_directory('.', 'admin.html')

# ===== API Endpoints =====

@app.route('/api/login', methods=['POST'])
def api_login():
    """API สำหรับเข้าสู่ระบบ"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    ip = request.remote_addr
    logging.info(f"Login attempt for user: {username} from IP: {ip}")
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400
    
    if username not in USERS or USERS[username] != password:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
    
    session.permanent = True
    session['user_id'] = username
    session['is_admin'] = (username == 'admin')
    
    return jsonify({
        'status': 'success',
        'message': f'Welcome {username}!',
        'is_admin': username == 'admin'
    })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API สำหรับออกจากระบบ"""
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out'})

@app.route('/api/user', methods=['GET'])
@login_required
def api_user():
    """API เพื่อดึงข้อมูลผู้ใช้ปัจจุบัน"""
    return jsonify({
        'user_id': session.get('user_id'),
        'is_admin': session.get('is_admin', False)
    })

@app.route('/api/products', methods=['GET'])
def api_products():
    """API เพื่อดึงรายการสินค้า"""
    products = load_products()
    return jsonify({'status': 'success', 'products': products})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def api_product_detail(product_id):
    """API เพื่อดึงรายละเอียดสินค้า"""
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            return jsonify({'status': 'success', 'product': product})
    return jsonify({'status': 'error', 'message': 'Product not found'}), 404

@app.route('/api/products/<int:product_id>/quantity', methods=['PUT'])
@admin_required
def api_update_quantity(product_id):
    """API เพื่อปรับแก้จำนวนสินค้า (Admin only)"""
    data = request.json
    new_quantity = data.get('quantity')
    
    if new_quantity is None or new_quantity < 0:
        return jsonify({'status': 'error', 'message': 'Invalid quantity'}), 400
    
    products = load_products()
    for product in products:
        if product['id'] == product_id:
            product['quantity'] = new_quantity
            save_products(products)
            return jsonify({
                'status': 'success',
                'message': f'Quantity updated to {new_quantity}',
                'product': product
            })
    
    return jsonify({'status': 'error', 'message': 'Product not found'}), 404

@app.route('/api/products', methods=['POST'])
@admin_required
def api_create_product():
    """API เพื่อสร้างสินค้าใหม่ (Admin only)"""
    data = request.json
    products = load_products()
    
    # หา ID สูงสุด
    max_id = max([p['id'] for p in products], default=0)
    
    new_product = {
        'id': max_id + 1,
        'name': data.get('name', 'Unnamed Product'),
        'price': data.get('price', 0),
        'quantity': data.get('quantity', 0),
        'description': data.get('description', '')
    }
    
    products.append(new_product)
    save_products(products)
    
    return jsonify({'status': 'success', 'product': new_product}), 201

if __name__ == '__main__':
    # สร้างไฟล์สินค้าเริ่มต้นถ้ายังไม่มี
    if not os.path.exists(PRODUCTS_FILE):
        save_products(get_default_products())
    
    app.run(port=8888, debug=True)