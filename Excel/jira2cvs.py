import pandas as pd

# HTML dosyasını oku
input_file = r'C:\Users\enesk\Downloads\jira.xls'  # Dosya aslında HTML
output_file = r'C:\Users\enesk\Downloads\jira.csv'

# HTML dosyasındaki tabloları oku
try:
    # HTML'deki tüm tabloları okur
    dfs = pd.read_html(input_file)
    
    # Eğer tablo bulunduysa
    if dfs:
        # İlk tabloyu seçin (birden fazla tablo olabilir)
        df = dfs[1]
        
        # DataFrame'i CSV olarak kaydet
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"{input_file} dosyası {output_file} olarak kaydedildi.")
    else:
        print("Dosyada tablo bulunamadı.")
except Exception as e:
    print(f"Hata: {e}")