import requests
import json
import os

API_KEY = "AIzaSyDum_znanDZfyMMiU3_23khHWhtEsk1bYQ"
MODEL = "models/gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL}:generateContent?key={API_KEY}"

def evolve_bot():
    # 1. قراءة كود المحلل الحالي
    analyzer_path = "src/analyzer.py"
    with open(analyzer_path, "r") as f:
        current_code = f.read()

    print("🤖 Gemini يقوم الآن بإعادة هندسة الكود...")

    # 2. إعداد الطلب لـ Gemini
    prompt = f"""
    أنت خبير في الربط البرمجي للمنصات (API Integration). 
    نحن نواجه مشكلة في تثبيت ccxt على Termux.
    
    المطلوب:
    1. أعِد كتابة ملف 'src/exchange_handler.py' ليتصل بمنصة Binance (أو أي منصة افتراضية) باستخدام مكتبة 'requests' فقط.
    2. نحتاج فقط لدالة جلب السعر الحالي (get_price) ودالة جلب الشموع الأخيرة (get_candles).
    3. لا تستخدم ccxt نهائياً. استخدم روابط REST API المباشرة.
    4. أرجع الكود الخام فقط بدون شرح.
    """
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    # 3. إرسال الطلب واستلام الكود المطور
    res = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    
    if res.status_code == 200:
        new_code = res.json()['candidates'][0]['content']['parts'][0]['text']
        
        # تنظيف الكود من علامات مارك داون (```python)
        new_code = new_code.replace("```python", "").replace("```", "").strip()

        # 4. حفظ الكود المطور في ملف جديد للاختبار
        with open("src/analyzer_v2.py", "w") as f:
            f.write(new_code)
        
        print("✅ تم إنشاء 'analyzer_v2.py' بنجاح! تفقد الملف لرؤية التعديلات.")
    else:
        print(f"❌ خطأ في التطوير: {res.text}")

if __name__ == "__main__":
    evolve_bot()

