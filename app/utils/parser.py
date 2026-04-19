# import json
# import re

# def parse_llm_response(result):
#     try:
#         content = result.get("response") or result

#         # 🔥 hapus ```json ... ```
#         content = re.sub(r"```json\n|\n```", "", content)

#         parsed = json.loads(content)

#         return parsed.get("footballs", [])

#     except Exception as e:
#         raise Exception(f"Invalid JSON from LLM: {str(e)}")

import json
import re

def parse_llm_response(response_data):
    try:
        # 1. Cek apakah inputnya Dictionary atau String
        # Jika Dictionary (seperti log kamu), ambil isi dari key 'response'
        if isinstance(response_data, dict):
            text_to_parse = response_data.get('response', '')
        else:
            text_to_parse = str(response_data)

        print("Teks yang akan diproses:", text_to_parse)

        # 2. Bersihkan blok kode markdown (```json ... ```)
        clean_text = re.sub(r'```json|```', '', text_to_parse).strip()
        
        # 3. Cari pola JSON { ... }
        match = re.search(r'\{.*\}', clean_text, re.DOTALL)
        if match:
            clean_text = match.group(0)
            
        data = json.loads(clean_text)
        
        # 4. Ambil list dari key "clubs"
        return data.get("clubs", [])
        
    except Exception as e:
        print(f"Gagal parsing: {e}")
        return []