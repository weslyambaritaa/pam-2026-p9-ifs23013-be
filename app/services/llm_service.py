import requests
from app.config import Config

def generate_from_llm(prompt: str):
    api_key = Config.GEMINI_API_KEY
    # Menggunakan model gemini-1.5-flash yang super cepat dan gratis
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # Struktur body request sesuai dokumentasi resmi Gemini
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    if response.status_code != 200:
        print("ERROR DARI GEMINI:", response.text)
        raise Exception(f"Gemini API gagal dengan status {response.status_code}")

    data = response.json()

    try:
        # Mengambil teks jawaban dari dalam struktur JSON Gemini
        answer_text = data['candidates'][0]['content']['parts'][0]['text']
        
        # Kita bungkus dalam dictionary {"response": ...} 
        # agar app/utils/parser.py Anda tetap bisa membacanya tanpa perlu diubah!
        return {"response": answer_text}
        
    except Exception as e:
        print("GAGAL PARSING RESPON GEMINI:", data)
        raise Exception("Gagal membaca format teks dari Gemini")