import pandas as pd
import re

# CSV dosyasını oku ve temizle (önceki adımlardan)
df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv')

def clean_description(text):
    if pd.isnull(text):
        return text
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.lower()
    return text

df['cleaned_Description'] = df['Description'].apply(clean_description)

def extract_features(text):
    if pd.isnull(text):
        return pd.Series({
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0
        })
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip() != '']
    sentence_count = len(sentences)
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    return pd.Series({
        'char_count': char_count,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length
    })

df[['char_count', 'word_count', 'sentence_count', 'avg_word_length']] = df['cleaned_Description'].apply(extract_features)

# Kalite ölçütlerine dayalı basit bir puanlama fonksiyonu tanımlıyoruz.
def quality_score(row):
    score = 0
    # Örnek kriter 1: Kelime sayısı en az 10 olmalı.
    if row['word_count'] >= 30:
        score += 1
    # Örnek kriter 2: Cümle sayısı en az 1 olmalı.
    if row['sentence_count'] >= 3:
        score += 1
    # Örnek kriter 3: Ortalama kelime uzunluğu 4 karakter veya daha fazla olmalı.
    if row['avg_word_length'] >= 4:
        score += 1
    
    # Toplam puana göre kalite etiketlemesi:
    if score == 3:
        return 'High'
    elif score == 2:
        return 'Medium'
    else:
        return 'Low'

df['quality'] = df.apply(quality_score, axis=1)

# Sonuçları kontrol edelim:
print(df[['cleaned_Description', 'word_count', 'sentence_count', 'avg_word_length', 'quality']])
