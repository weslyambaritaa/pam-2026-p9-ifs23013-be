import requests
from app.config import Config

def generate_from_llm(prompt: str):
    api_key = Config.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    
    print("\n[LLM] Mengirim request ke Gemini...") # LOG 1
    
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json=payload
    )

    print(f"[LLM] Status Response: {response.status_code}") # LOG 2
    
    if response.status_code != 200:
        print(f"[LLM] BODY ERROR: {response.text}") # LOG 3
        raise Exception(f"Gemini API gagal dengan status {response.status_code}")

    data = response.json()
    
    try:
        answer_text = data['candidates'][0]['content']['parts'][0]['text']
        print(f"[LLM] Balasan Gemini:\n{answer_text}") # LOG 4
        return {"response": answer_text}
    except Exception as e:
        print(f"[LLM] Format JSON tidak sesuai dugaan: {data}")
        raise Exception("Gagal membaca struktur data dari Gemini")