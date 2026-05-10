import requests
import json

API_KEY = "AIzaSyDum_znanDZfyMMiU3_23khHWhtEsk1bYQ"

def find_and_ask_gemini():
    # 1. الاستعلام عن الموديلات المتاحة لمفتاحك
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        r = requests.get(list_url)
        if r.status_code != 200:
            print(f"❌ خطأ في المفتاح: {r.text}")
            return

        models = r.json().get('models', [])
        # البحث عن أي موديل يحتوي اسم gemini
        available_models = [m['name'] for m in models if 'gemini' in m['name'] and 'generateContent' in m['supportedGenerationMethods']]
        
        if not available_models:
            print("❌ لم يتم العثور على أي موديلات Gemini مفعلة في حسابك.")
            return

        # اختيار أول موديل متاح (غالباً سيكون gemini-1.5-flash أو gemini-pro)
        target_model = available_models[0]
        print(f"✅ تم العثور على الموديل: {target_model}")

        # 2. إرسال السؤال للموديل الذي وجدناه
        ask_url = f"https://generativelanguage.googleapis.com/v1beta/{target_model}:generateContent?key={API_KEY}"
        data = {"contents": [{"parts": [{"text": "Hello, this is KAIROS project. Are you ready?"}]}]}
        
        res = requests.post(ask_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        
        if res.status_code == 200:
            print("🚀 استجابة Gemini:")
            print(res.json()['candidates'][0]['content']['parts'][0]['text'])
        else:
            print(f"❌ خطأ عند التحدث مع الموديل: {res.text}")

    except Exception as e:
        print(f"📡 خطأ في الاتصال: {e}")

find_and_ask_gemini()

