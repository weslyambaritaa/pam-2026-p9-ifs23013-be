import json
import re

def parse_llm_response(result):
    content = result.get("response") or result
    try:
        # Bersihkan markdown json jika AI masih membandel mengirimkannya
        content = re.sub(r"```json\n?", "", content)
        content = re.sub(r"```\n?", "", content)
        
        # Ambil HANYA teks dari kurung kurawal pertama { hingga terakhir }
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            content = content[start_idx:end_idx+1]

        parsed = json.loads(content)

        return parsed.get("motivations", [])

    except Exception as e:
        # Buka komentar print di bawah ini jika masih error 
        # print(f"\n--- TEKS YANG GAGAL DIPARSING ---\n{content}\n---------------------------------\n")
        raise Exception(f"Invalid JSON from LLM: {str(e)}")