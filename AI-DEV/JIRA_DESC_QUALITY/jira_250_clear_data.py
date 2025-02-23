import pandas as pd
import re

df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv')

def clean_description(text):
    if pd.isnull(text):
        return text
    # HTML tag'lerini temizle
    text = re.sub(r'<.*?>', '', text)
    # Türkçe karakterler dahil olmak üzere, sadece belirlenen karakterleri koru
    text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()-]', '', text)
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    # Metni küçük harfe çevir
    text = text.lower()
    return text

df['cleaned_Description'] = df['Description'].apply(clean_description)

print(df[['Description', 'cleaned_Description']].head())
