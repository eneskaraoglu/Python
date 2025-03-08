import spacy
import pandas as pd
import re
from spacy.lang.tr.stop_words import STOP_WORDS

# Türkçe Transformer modelini yükle
nlp = spacy.load("tr_core_news_trf")

# CSV dosyasını oku
df = pd.read_csv(r'C:\ANALIZ_DATA\jira_min.csv')

# Metin temizleme ve stopwords kaldırma fonksiyonu
def clean_description(text):
    if pd.isnull(text):
        return text

    # HTML etiketlerini temizle
    text = re.sub(r'<.*?>', '', text)
    
    # Özel karakterleri temizle ama bazı işaretleri koru
    text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s]', '', text)
    
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()

    # Stopwords temizleme işlemi (spaCy kullanarak)
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if token.text.lower() not in STOP_WORDS]
    filtered_tokens = [token.lemma_ for token in doc if token.pos_ in {"NOUN", "VERB"}]

    return ' '.join(filtered_tokens)  # Stopwords çıkarılmış metni döndür

# Description sütununu temizle ve stopwords'leri kaldır
df['cleaned_Description'] = df['Description'].apply(clean_description)

# Temizlenmiş metinleri işle
for text in df['cleaned_Description']:
    #print(f"text: {text}")
    if pd.isnull(text):
        continue
    doc = nlp(text)
    
    # Kelimeleri ve kök halleri
    for token in doc:
        print(f"Kelime: {token.text}, Kök: {token.lemma_}, POS: {token.pos_}")
    
    # Varlıkları bul
    for ent in doc.ents:
        print(f"Varlık: {ent.text}, Türü: {ent.label_}")

from collections import Counter
from itertools import islice

def get_ngrams(text, n=2):
    words = text.split()
    ngrams = zip(*[islice(words, i, None) for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

ngrams_list = []
for text in df['cleaned_Description'].dropna():
    ngrams_list.extend(get_ngrams(text, 2))  # Bigram

ngram_counts = Counter(ngrams_list)
print(ngram_counts.most_common(10))  # En sık geçen 10 bigram

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="dbmdz/bert-base-turkish-uncased")
sentiments = df['cleaned_Description'].dropna().apply(lambda x: sentiment_pipeline(x)[0])

df['Sentiment'] = sentiments.apply(lambda x: x['label'])
df['Confidence'] = sentiments.apply(lambda x: x['score'])

print(df[['cleaned_Description', 'Sentiment', 'Confidence']].head())
