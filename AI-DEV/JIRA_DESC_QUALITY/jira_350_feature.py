import pandas as pd
import re

# CSV dosyasını ve temizlenmiş açıklamaları daha önce oluşturduğumuzu varsayıyoruz:
df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv')

# Daha önceki adımda Türkçe karakterleri koruyarak temizlenmiş sütunu oluşturduğumuzu düşünelim:
def clean_description(text):
    if pd.isnull(text):
        return text
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    return text

df['cleaned_Description'] = df['Description'].apply(clean_description)

# Özellik çıkarımı için bir fonksiyon tanımlıyoruz:
def extract_features(text):
    if pd.isnull(text):
        return pd.Series({
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0
        })
    # Karakter sayısı
    char_count = len(text)
    # Kelime sayısı: Basit bir boşluk bazlı ayrım
    words = text.split()
    word_count = len(words)
    # Cümle sayısı: Nokta, ünlem ve soru işaretlerini cümle ayırıcı olarak kullanıyoruz
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip() != '']
    sentence_count = len(sentences)
    # Ortalama kelime uzunluğu
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    return pd.Series({
        'char_count': char_count,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length
    })

# Özellikleri çıkarıp DataFrame'e ekliyoruz:
df[['char_count', 'word_count', 'sentence_count', 'avg_word_length']] = df['cleaned_Description'].apply(extract_features)

# Sonuçları kontrol etmek için ilk 5 satırı görüntüleyelim:
print(df[['cleaned_Description', 'char_count', 'word_count', 'sentence_count', 'avg_word_length']].head())
