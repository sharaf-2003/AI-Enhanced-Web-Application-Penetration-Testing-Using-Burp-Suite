# ai_request_analyzer.py
import re
import sys

def analyze_http_request(request_text):
    """تحليل طلب HTTP باستخدام قواعد AI بسيطة"""
    
    print("\n" + "=" * 60)
    print("🤖 AI Security Analysis Report")
    print("=" * 60)
    
    findings = []
    
    # 1. فحص Path Traversal
    if "../" in request_text or "..\\" in request_text or "%2e%2e" in request_text:
        findings.append("🔴 CRITICAL: Path Traversal detected!")
    
    # 2. فحص SQL Injection
    sql_patterns = ["'", '"', " OR 1=1", "OR '1'='1", "UNION SELECT", "DROP TABLE"]
    for pattern in sql_patterns:
        if pattern.lower() in request_text.lower():
            findings.append("⚠️ Possible SQL Injection: " + pattern)
            break
    
    # 3. فحص XSS
    xss_patterns = ["<script>", "alert(", "onerror=", "javascript:"]
    for pattern in xss_patterns:
        if pattern.lower() in request_text.lower():
            findings.append("⚠️ Possible XSS: " + pattern)
            break
    
    # 4. فحص Information Disclosure
    sensitive_endpoints = ["/credentials", "/captured_photos", "/admin", "/config", "/backup"]
    for endpoint in sensitive_endpoints:
        if endpoint in request_text:
            findings.append("🔴 Information Disclosure Risk: " + endpoint)
    
    # 5. فحص كشف المسار (Path Disclosure)
    if "Traceback" in request_text or "FileNotFoundError" in request_text:
        findings.append("🔴 Path Disclosure: Internal paths exposed")
    
    # 6. فحص Debug Mode
    if "debug=True" in request_text or "DEBUG" in request_text:
        findings.append("⚠️ Debug Mode Enabled")
    
    # عرض النتائج
    if findings:
        print("\n📋 Vulnerabilities Found:\n")
        for i, finding in enumerate(findings, 1):
            print(f"  {i}. {finding}")
    else:
        print("\n✅ No obvious vulnerabilities found in this request")
    
    print("\n" + "=" * 60)
    print("💡 Tip: Check the response as well for sensitive data leaks")
    print("=" * 60)

def main():
    print("🤖 AI HTTP Request Analyzer")
    print("Paste the HTTP request below (press Ctrl+D or Ctrl+Z when done):\n")
    
    # قراءة الطلب من المستخدم
    request_text = sys.stdin.read()
    
    if request_text.strip():
        analyze_http_request(request_text)
    else:
        print("❌ No request provided")

if __name__ == "__main__":
    main()