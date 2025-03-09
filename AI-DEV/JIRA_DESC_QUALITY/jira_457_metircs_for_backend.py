import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Temel stil ayarları
plt.style.use('default')  # seaborn yerine default stil kullanıyoruz
sns.set_theme()  # Seaborn'un varsayılan temasını kullan

# CSV dosyasını oku
df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv')

def clean_description(text):
    if pd.isnull(text):
        return text
    # HTML etiketlerini temizle
    text = re.sub(r'<.*?>', '', text)
    # Özel karakterleri temizle ama bazı işaretleri koru
    text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()[\]```\-*•]', '', text)
    # Fazla boşlukları temizle
    text = re.sub(r'\s+', ' ', text).strip()
    return text  # Artık lower() kullanmıyoruz çünkü büyük harfli kelimeleri saymak istiyoruz

def extract_features(text):
    if pd.isnull(text):
        return pd.Series({
            'char_count': 0,
            'word_count': 0,
            'sentence_count': 0,
            'avg_word_length': 0,
            #'technical_terms': 0,
            #'has_code_blocks': False,
            #'has_steps': False,
            'has_screenshots': False,
            'url_count': False,
            #'bullet_points': 0,
            'has_acceptance_criteria': False,
            'has_expected_result': False,
            'has_altsistem': False,
            'ekran_kodu' :False
        })

    # Temel metrikler
    char_count = len(text)
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip() != '']
    sentence_count = len(sentences)
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

    # Yeni metrikler
    #technical_terms = len([w for w in words if w.isupper() and len(w) > 1])
    #has_code_blocks = '```' in text
    #has_steps = bool(re.search(r'(\d+\.|adım|step)', text.lower()))
    has_screenshots = bool(re.search(r'(\[image\]|\.png|\.jpg|\.jpeg|\.gif)', text.lower()))
    url_count = bool(re.search(r'(\d+\.|http|www)', text.lower())) 
    #bullet_points = text.count('•') + text.count('- ') + text.count('* ')
    has_acceptance_criteria = 'kabul kriterleri' in text.lower() or 'örne' in text.lower() or 'meli' in text.lower() or 'malı' in text.lower()
    has_expected_result = 'olmalı' in text.lower() or 'yapılma' in text.lower() or 'yapabilir' in text.lower()  or 'yardım' in text.lower() or 'çözüm' in text.lower()  or 'öneri' in text.lower() or 'bug' in text.lower()  or 'isten' in text.lower() or 'edil' in text.lower() 
    has_altsistem = 'stok' in text.lower() or 'kalite' in text.lower() or 'finans' in text.lower() or 'üretim' in text.lower() or 'satış' in text.lower() or 'satınalma' in text.lower()  or 'kalite' in text.lower() or 'bakım' in text.lower()
    
    return pd.Series({
        'char_count': char_count,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length,
        #'technical_terms': technical_terms,
        #'has_code_blocks': has_code_blocks,
        #'has_steps': has_steps,
        'has_screenshots': has_screenshots,
        'url_count': url_count,
        #'bullet_points': bullet_points,
        'has_acceptance_criteria': has_acceptance_criteria,
        'has_expected_result': has_expected_result,
        'has_altsistem': has_altsistem
    })

# Temizlenmiş açıklamaları ve özellikleri oluştur
df['cleaned_Description'] = df['Description'].apply(clean_description)
df = pd.concat([df, df['cleaned_Description'].apply(extract_features)], axis=1)

# Sorumlu kişi belirleme
df['final_responsible'] = df['Sorumlu Geliştirici'].fillna('')
df.loc[df['final_responsible'] == '', 'final_responsible'] = df['Creator']

def quality_score(row):
    
    score = 0 
    if row['word_count'] >= 30: score += 1
    if row['word_count'] >= 60: score += 1
    if row['sentence_count'] >= 3: score += 1
    if row['avg_word_length'] >= 4: score += 1
    #if row['technical_terms'] > 0: score += 1
    #if row.get('has_code_blocks', False): score += 1
    #if row['has_steps']: score += 1
    if row['has_screenshots']: score += 1
    #if row['bullet_points'] > 0: score += 1
    if row['has_acceptance_criteria']: score += 2
    if row['has_expected_result']: score += 3
    if row['has_altsistem']: score += 1
    if row['url_count']: score += 1
    if row['Creator'] == row['final_responsible']: score -= 1
    if row['Ekran Kodu'] != "":  score += 1


    # Toplam puana göre kalite değerlendirmesi
    if score >= 7:
        quality = 'High'
    elif score >= 4:
        quality = 'Medium'
    else:
        quality = 'Low'
    return pd.Series({'quality': quality, 'score': score})

df[['quality', 'score']] = df.apply(quality_score, axis=1)



# jira_457_upgrade_metircs_graph.py içinde:
class JiraAnalyzer:
    def __init__(self, df=None):
        self.df = df

    def clean_description(self, text):
        """Metni temizleyen fonksiyon"""
        if pd.isnull(text):
            return text
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-zA-Z0-9çÇğĞıİöÖşŞüÜ\s.,;:!?()[\]```\-*•]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_features(self, text):
        """Metinden özellik çıkaran fonksiyon"""
        if pd.isnull(text):
            return pd.Series({
                'char_count': 0,
                'word_count': 0,
                'sentence_count': 0,
                'avg_word_length': 0,
                'has_screenshots': False,
                'url_count': False,
                'has_acceptance_criteria': False,
                'has_expected_result': False,
                'has_altsistem': False
            })

        char_count = len(text)
        words = text.split()
        word_count = len(words)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip() != '']
        sentence_count = len(sentences)
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0

        has_screenshots = bool(re.search(r'(\[image\]|\.png|\.jpg|\.jpeg|\.gif)', text.lower()))
        url_count = bool(re.search(r'(\d+\.|http|www)', text.lower()))
        has_acceptance_criteria = 'kabul kriterleri' in text.lower() or 'meli' in text.lower() or 'malı' in text.lower()
        has_expected_result = 'olmalı' in text.lower() or 'çözüm' in text.lower()
        has_altsistem = any(x in text.lower() for x in ['stok', 'kalite', 'finans', 'üretim', 'satış', 'satınalma'])

        return pd.Series({
            'char_count': char_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_word_length': avg_word_length,
            'has_screenshots': has_screenshots,
            'url_count': url_count,
            'has_acceptance_criteria': has_acceptance_criteria,
            'has_expected_result': has_expected_result,
            'has_altsistem': has_altsistem
        })
