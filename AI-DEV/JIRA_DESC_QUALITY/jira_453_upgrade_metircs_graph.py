import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

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
            'technical_terms': 0,
            'has_code_blocks': False,
            'has_steps': False,
            'has_screenshots': False,
            'url_count': 0,
            'bullet_points': 0,
            'has_acceptance_criteria': False,
            'has_expected_result': False,
            'has_altsistem': False
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
    technical_terms = len([w for w in words if w.isupper() and len(w) > 1])
    #has_code_blocks = '```' in text
    has_steps = bool(re.search(r'(\d+\.|adım|step)', text.lower()))
    has_screenshots = bool(re.search(r'(\[image\]|\.png|\.jpg|\.jpeg|\.gif)', text.lower()))
    url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
    bullet_points = text.count('•') + text.count('- ') + text.count('* ')
    has_acceptance_criteria = 'kabul kriterleri' in text.lower() or 'örnek' in text.lower() or 'örneğin' in text.lower()
    has_expected_result = 'olmalı' in text.lower() or 'istenen' in text.lower() or 'isteniyor' in text.lower()
    has_altsistem = 'stok' in text.lower() or 'kalite' in text.lower() or 'finans' in text.lower() or 'üretim' in text.lower() or 'satış' in text.lower() or 'satınalma' in text.lower()
    
    return pd.Series({
        'char_count': char_count,
        'word_count': word_count,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length,
        'technical_terms': technical_terms,
        #'has_code_blocks': has_code_blocks,
        'has_steps': has_steps,
        'has_screenshots': has_screenshots,
        'url_count': url_count,
        'bullet_points': bullet_points,
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
    #if row['final_responsible'] == row['Creator']:
    #    return 'Low'
    
    score = 0
    
    # Temel kriterler
    if row['word_count'] >= 30: score += 1
    if row['sentence_count'] >= 3: score += 1
    if row['avg_word_length'] >= 4: score += 1
    
    # Yeni kriterler
    if row['technical_terms'] > 0: score += 1
    if row['has_code_blocks']: score += 1
    if row['has_steps']: score += 1
    if row['has_screenshots']: score += 1
    if row['bullet_points'] > 0: score += 1
    if row['has_acceptance_criteria']: score += 1
    if row['has_expected_result']: score += 1
    if row['has_altsistem']: score += 1
    
    # Toplam puan üzerinden kalite değerlendirmesi
    if score >= 7:
        return 'High'
    elif score >= 4:
        return 'Medium'
    else:
        return 'Low'

df['quality'] = df.apply(quality_score, axis=1)

# Görselleştirmeler
# 1. Kalite Dağılımı
plt.figure(figsize=(10, 6))
colors = {'High': '#2ecc71', 'Medium': '#f1c40f', 'Low': '#e74c3c'}
quality_counts = df['quality'].value_counts().reindex(['High', 'Medium', 'Low'])
ax = quality_counts.plot(kind='bar', color=[colors[x] for x in quality_counts.index])
plt.title('JIRA Kalite Dağılımı', pad=20)
plt.xlabel('Kalite Seviyesi')
plt.ylabel('JIRA Sayısı')
for i, v in enumerate(quality_counts):
    ax.text(i, v, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# 2. Creator bazında Low kalite dağılımı
plt.figure(figsize=(12, 6))
low_quality = df[df['quality'] == 'Low']['Creator'].value_counts().head(10)
sns.barplot(x=low_quality.index, y=low_quality.values, palette='rocket')
plt.title('En Çok Low Kalite JIRA Oluşturan 10 Kullanıcı', pad=20)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Creator')
plt.ylabel('Low Kalite JIRA Sayısı')
plt.tight_layout()
plt.show()

# 3. Özellik bazında analiz
feature_cols = ['has_altsistem', 'has_steps', 'has_screenshots', 
                'has_acceptance_criteria', 'has_expected_result']
feature_stats = df[feature_cols].mean() * 100  # Yüzdelik değere çevir
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_stats.index, y=feature_stats.values, palette='viridis')
plt.title('Özellik Kullanım Oranları', pad=20)
plt.ylabel('Kullanım Oranı (%)')
plt.xticks(rotation=45, ha='right')
# Yüzde değerlerini çubukların üzerine ekle
for i, v in enumerate(feature_stats):
    plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom')
plt.tight_layout()
plt.show()

# 4. Yeni grafik: Kelime sayısı dağılımı
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='word_count', bins=30, kde=True)
plt.title('JIRA Açıklamalarındaki Kelime Sayısı Dağılımı', pad=20)
plt.xlabel('Kelime Sayısı')
plt.ylabel('JIRA Sayısı')
plt.axvline(x=30, color='r', linestyle='--', label='Minimum Beklenen (30)')
plt.legend()
plt.tight_layout()
plt.show()

# Detaylı analiz raporu
print("\n=== Detaylı Analiz Raporu ===")
print(f"\nToplam JIRA Sayısı: {len(df)}")
print("\nKalite Dağılımı:")
quality_percentages = df['quality'].value_counts(normalize=True).multiply(100).round(2)
for quality, percentage in quality_percentages.items():
    print(f"{quality}: {percentage}%")

print("\nOrtalama Metrikler:")
metrics = ['word_count', 'sentence_count', 'technical_terms', 'bullet_points']
for metric in metrics:
    print(f"{metric}: {df[metric].mean():.2f}")

print("\nÖzellik Kullanım Oranları:")
for feature in feature_cols:
    percentage = df[feature].mean() * 100
    print(f"{feature}: {percentage:.2f}%")

# En problematik kullanıcılar (en çok düşük kaliteli JIRA oluşturanlar)
print("\nEn Çok Düşük Kaliteli JIRA Oluşturan Kullanıcılar (Top 5):")
low_quality_creators = df[df['quality'] == 'Low']['Creator'].value_counts().head(5)
for creator, count in low_quality_creators.items():
    print(f"{creator}: {count} adet Low kalite JIRA")