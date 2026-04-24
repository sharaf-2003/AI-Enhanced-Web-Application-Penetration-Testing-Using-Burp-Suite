# AI-Enhanced-Web-Application-Penetration-Testing-Using-Burp-Suite
AI-Enhanced Web Application Penetration Testing Using Burp Suite
# 🤖 AI-Powered Penetration Testing with Burp Suite

## المشروع
دمج أداة الذكاء الاصطناعي مع أداة اختبار الاختراق Burp Suite لتحديد الثغرات الأمنية في تطبيق ويب تم تطويره خصيصًا لأغراض تعليمية.

## البيئة المستخدمة
| المكون | التفاصيل |
|--------|----------|
| **المضيف** | Windows 11 (تشغيل السيرفر) |
| **الجهاز الافتراضي** | Kali Linux (أدوات الاختبار) |
| **التطبيق المستهدف** | Flask server (`captcha_server.py`) |
| **أداة الاختراق** | Burp Suite Community |
| **أداة الذكاء الاصطناعي** | `ai_request_analyzer.py` (تحليل الطلبات) |

## الثغرات المكتشفة
| # | الثغرة | الخطورة |
|---|--------|----------|
| 1 | Path Traversal | 🔴 Critical |
| 2 | Information Disclosure (/credentials) | 🔴 Critical |
| 3 | Information Disclosure (/captured_photos) | 🟠 High |
| 4 | Debug Mode Enabled | 🟡 Medium |

## طريقة الدمج
1. تشغيل Burp Suite كـ Proxy على `127.0.0.1:8080`
2. تكوين متصفح Firefox لاستخدام الـ Proxy
3. تصفح التطبيق المستهدف عبر Burp
4. نسخ الطلبات من `HTTP history`
5. لصق الطلبات في `ai_request_analyzer.py`
6. الـ AI يقوم بتحليل الطلبات واكتشاف الثغرات

## نتائج التحليل
============================================================
🤖 AI Security Analysis Report
============================================================

📋 Vulnerabilities Found:

🔴 CRITICAL: Path Traversal detected!

🔴 Information Disclosure Risk: /credentials

🔴 Information Disclosure Risk: /captured_photos

============================================================
💡 Tip: Check the response as well for sensitive data leaks
============================================================


## التوصيات
- إزالة واجهات `/credentials` و `/captured_photos` أو إضافة مصادقة
- تنقية المدخلات لمنع Path Traversal
- إيقاف Debug Mode في بيئة الإنتاج (`debug=False`)
- استخدام HTTPS بدلاً من HTTP

## كيفية التشغيل
```bash
# على Kali Linux
git clone https://github.com/yourusername/ai-burp-integration.git
cd ai-burp-integration
python3 ai_request_analyzer.py

المؤلف
[شرف الدين نصال نمر] - مشروع لتوضيح دمج الذكاء الاصطناعي في اختبار الاختراق الأخلاقي
