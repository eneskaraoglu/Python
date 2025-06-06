import json
import requests
import time
from tqdm import tqdm

OLLAMA_URL = "http://localhost:11434/api/generate"
LLAMA_MODEL = "llama3.1"

def is_valid_qa(q, a):
    q = q.strip() if q else ""
    a = a.strip() if a else ""
    if not q or not a or len(q) < 8:
        return False
    return True

def is_distinct(q1, q2):
    return q1.strip().lower() != q2.strip().lower()

def paraphrase_with_ollama(question, n=5, retry=3):
    prompt = (
        f"Aşağıdaki sorunun anlamını değiştirmeden Türkçe olarak {n} farklı yeni soru oluştur. "
        f"Sadece yeni soruları numaralandırılmış liste halinde yaz:\n"
        f"Soru: {question}\n"
    )
    for _ in range(retry):
        try:
            payload = {
                "model": LLAMA_MODEL,
                "prompt": prompt,
                "options": {"temperature": 0.7, "num_predict": 512},
                "stream": False
            }
            resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
            if resp.status_code == 200:
                output = resp.json()['response']
                lines = [l.strip() for l in output.split("\n") if l.strip()]
                results = []
                for line in lines:
                    if line[0].isdigit() and (line[1] == '.' or line[1] == ')'):
                        q = line.split('.', 1)[-1].strip() if '.' in line else line.split(')', 1)[-1].strip()
                        results.append(q)
                if len(results) < n:
                    results = [l for l in lines if l and not l.lower().startswith('soru')]
                results = [pq for pq in results if pq and len(pq) > 8]
                return results[:n]
            else:
                print(f"API hata kodu: {resp.status_code}")
        except Exception as e:
            print("Hata oldu, tekrar deneniyor:", e)
            time.sleep(2)
    return []

# Dosyaları baştan oluştur (veya append modda aç)
main_file = open("llama_training_data_35b.jsonl", "a", encoding="utf-8")
error_log = open("parafraz_hatalar_log.jsonl", "a", encoding="utf-8")

with open("llama_training_data_7b_working.jsonl", "r", encoding="utf-8") as f:
    dataset = [json.loads(line) for line in f]

for item in tqdm(dataset):
    q = item.get('instruction', item.get('question'))
    a = item.get('output', item.get('answer'))
    # Orijinal soruyu yaz
    if is_valid_qa(q, a):
        main_file.write(json.dumps({'instruction': q, 'output': a}, ensure_ascii=False) + "\n")
    else:
        error_log.write(json.dumps({'error': 'orijinal_kayıt_hatalı', 'instruction': q, 'output': a}, ensure_ascii=False) + "\n")

    paraphrases = paraphrase_with_ollama(q, n=5)
    for pq in paraphrases:
        if is_valid_qa(pq, a) and is_distinct(pq, q):
            main_file.write(json.dumps({'instruction': pq, 'output': a}, ensure_ascii=False) + "\n")
        else:
            error_log.write(json.dumps({'error': 'parafraz_hatalı', 'parafraz': pq, 'orijinal': q, 'output': a}, ensure_ascii=False) + "\n")
    main_file.flush()  # Her adımda dosyaya yazma garantili olsun
    error_log.flush()
    time.sleep(1)

main_file.close()
error_log.close()

print("Tüm kayıtlar anlık olarak kaydedildi. Hatalı kayıtlar 'parafraz_hatalar_log.jsonl' dosyasına loglandı.")
