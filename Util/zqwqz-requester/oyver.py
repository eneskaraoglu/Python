import requests
import time  # Bekleme için gerekli modül

# URL'yi belirtin (istek gönderilecek adres)
url = "https://zqwqz.org/oyver"

# İstek başlıkları (headers) - sunucuya gönderilen meta bilgiler
headers_template = {
    "accept": "*/*",  # Sunucudan herhangi bir içerik türünü kabul ettiğimizi belirtir
    "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",  # Tercih edilen diller
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",  # Gönderilen verinin formatı
    "cookie": "PHPSESSID=3fe8e1bnqkbc0oscddek5dq0io; SL_G_WPT_TO=tr; SL_GWPT_Show_Hide_tmp=1; browserHash=5e0df38b78670a8159a8486f1675e828; SL_wptGlobTipTmp=1; guser=4b45b2b22d86b3381d3d67d0b732952c; newsChecked=false",  # Oturum bilgileri
    "origin": "https://zqwqz.org",  # İstek kaynağını belirtir (CORS için)
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',  # Tarayıcı bilgisi
    "sec-ch-ua-mobile": "?0",  # Mobil cihaz kullanılmadığını belirtir
    "sec-ch-ua-platform": '"Windows"',  # İşletim sistemi
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",  # Tarayıcı tanımlayıcı bilgisi
    "x-requested-with": "XMLHttpRequest",  # AJAX isteklerini belirtmek için kullanılır
}

# Döngü için başlangıç ve bitiş ID'si
start_id = 280  # Başlangıç ID
end_id = 1350    # Bitiş ID

# Döngü - Belirtilen aralıkta ardışık istekler gönderilir
for pid in range(start_id, end_id + 1):
    # Dinamik referer URL'si oluştur
    referer = f"https://zqwqz.org/muzik/dinle/zikuvikuzi-blow-{pid}"
    
    # Headers içine dinamik referer ekle
    headers = headers_template.copy()
    headers["referer"] = referer  # Dinamik referer ekleniyor

    # POST verisi (body) - Sunucuya gönderilen veriler
    data = {
        "pid": pid,      # Puan verilen içerik ID'si
        "puan": 5,       # Verilen puan (örneğin, 5 puan)
        "type": "puanver",  # İşlem türü
        "t": "muzik",    # İçerik türü
    }

    # POST isteğini gönder
    response = requests.post(url, headers=headers, data=data)

    # İstek yanıtını kontrol et ve ekrana yazdır
    if response.status_code == 200:
        print(f"PID: {pid} için istek başarıyla gönderildi. Referer: {referer}")
    else:
        print(f"PID: {pid} için istek başarısız oldu. Durum Kodu: {response.status_code}")

    for remaining in range(65, 0, -1):  # 65'ten geriye doğru sayar
        print(f"PID:{pid}--->{remaining} saniye kaldı...", end="\r", flush=True)
        time.sleep(1)  # Her bir saniye bekle
    print(" ")  # Satırı temizle
