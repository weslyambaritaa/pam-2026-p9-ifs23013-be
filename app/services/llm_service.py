# import requests
# from app.config import Config

# def generate_from_llm(prompt: str):
#     response = requests.post(
#         f"{Config.BASE_URL}/llm/chat",
#         json={
#             "token": Config.LLM_TOKEN,
#             "chat": prompt
#         }
#     )
    
#     # Debug Output dari API LLM
#     # print("STATUS:", response.status_code)
#     # print("RESPONSE:", response.text)

#     if response.status_code != 200:
#         raise Exception("LLM request failed")

#     return response.json()

import requests
from app.config import Config

def generate_from_llm(prompt: str):
    api_key = Config.LLM_TOKEN
    
    # Menggunakan endpoint resmi Google Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    # Format JSON payload yang diwajibkan oleh Google
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    # Debug jika terjadi error dari sisi Google
    if response.status_code != 200:
        print("ERROR DARI GEMINI:", response.text)
        raise Exception("Google Gemini API request failed")

    data = response.json()
    
    try:
        # Menelusuri hasil JSON dari Gemini untuk mendapatkan teks jawabannya
        answer_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Mengembalikan dalam format yang dikenali oleh parser.py Anda
        return {"response": answer_text}
        
    except (KeyError, IndexError) as e:
        raise Exception(f"Gagal membaca format response Gemini: {str(e)}")