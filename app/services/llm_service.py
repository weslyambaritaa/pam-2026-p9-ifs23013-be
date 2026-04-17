import requests
from app.config import Config

def generate_from_llm(prompt: str):
    api_key = Config.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    # FIX: Tambahkan generationConfig untuk memaksa format respon menjadi JSON murni
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    if response.status_code != 200:
        print("ERROR DARI GEMINI:", response.text) # Muncul di terminal jika API Key salah
        raise Exception(f"Gemini API gagal dengan status {response.status_code}")

    data = response.json()

    try:
        answer_text = data['candidates'][0]['content']['parts'][0]['text']
        return {"response": answer_text}
        
    except Exception as e:
        print("GAGAL MEMBACA DATA GEMINI:", data)
        raise Exception("Gagal membaca format teks dari Gemini")