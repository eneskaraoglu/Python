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

# Görselleştirmeler
# 1. Kalite Dağılımı
plt.figure(figsize=(10, 6))
# Renk paletini Undefined için de ekleyin
colors = {
    'High': '#2ecc71',
    'Medium': '#f1c40f',
    'Low': '#e74c3c',
    'Undefined': '#95a5a6'
}
# Kategori sırasını güncelleyip, olmayan kategoriler için fill_value kullanın
quality_counts = df['quality'].value_counts().reindex(['High', 'Medium', 'Low'], fill_value=0)
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

# 2. Creator bazında Low kalite dağılımı
plt.figure(figsize=(12, 6))
low_quality = df[df['quality'] == 'High']['Creator'].value_counts().head(10)
sns.barplot(x=low_quality.index, y=low_quality.values, palette='rocket')
plt.title('En Çok High Kalite JIRA Oluşturan 10 Kullanıcı', pad=20)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Creator')
plt.ylabel('High Kalite JIRA Sayısı')
plt.tight_layout()
plt.show()

# Creator bazında Undefined JIRA sayısı
undefined_counts = df[df['quality'] == 'Undefined']['Creator'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=undefined_counts.index, y=undefined_counts.values, palette='gray')
plt.title('En Çok Undefined JIRA Oluşturan Kullanıcılar', pad=20)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Creator')
plt.ylabel('Undefined JIRA Sayısı')
plt.tight_layout()
plt.show()


# 3. Özellik bazında analiz
feature_cols = ['has_altsistem', 'url_count', 'has_screenshots', 
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

# 4. Yeni grafik: Kelime sayısı dağılımı (300'e kadar, fazlası toplu)
plt.figure(figsize=(10, 6))

# Veriyi 300 kelimeden az ve çok olarak ayır
df_under_300 = df[df['word_count'] <= 300].copy()
df_over_300 = df[df['word_count'] > 300].copy()

# 300'e kadar olan verileri hist plot ile göster
sns.histplot(data=df_under_300, x='word_count', bins=30, kde=True)

# 300'den fazla olan verilerin sayısını kontrol et
if len(df_over_300) > 0:
    # 300'den fazla kelimesi olan JIRA'ların sayısını göster
    plt.text(250, plt.gca().get_ylim()[1]*0.9, 
             f"300'den fazla kelimesi olan: {len(df_over_300)} JIRA", 
             bbox=dict(facecolor='red', alpha=0.2))

plt.title('JIRA Açıklamalarındaki Kelime Sayısı Dağılımı (max 300)', pad=20)
plt.xlabel('Kelime Sayısı')
plt.ylabel('JIRA Sayısı')
plt.axvline(x=30, color='r', linestyle='--', label='Minimum Beklenen (30)')
plt.xlim(0, 300)  # X eksenini 0-500 arası ile sınırla
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
metrics = ['word_count', 'sentence_count', 'has_screenshots', 'url_count']
for metric in metrics:
    print(f"{metric}: {df[metric].mean():.2f}")

print("\nÖzellik Kullanım Oranları:")
for feature in feature_cols:
    percentage = df[feature].mean() * 100
    print(f"{feature}: {percentage:.2f}%")

# En problematik kullanıcılar (en çok düşük kaliteli JIRA oluşturanlar)
print("\nEn Çok Düşük Kaliteli JIRA Oluşturan Kullanıcılar (Top 5):")
low_quality_creators = df[df['quality'] == 'Low']['Creator'].value_counts().head(5)

# Tüm creator'lar için Low ve Undefined JIRA sayılarını hesaplayalım
low_quality = df[df['quality'] == 'Low']['Creator'].value_counts()
medium_quality = df[df['quality'] == 'Medium']['Creator'].value_counts()
high_quality = df[df['quality'] == 'High']['Creator'].value_counts()


# İki değeri toplayarak her Creator için combined_count hesaplayalım
combined = low_quality.add(medium_quality, fill_value=0).add(high_quality, fill_value=0)

# En yüksek combined değere sahip ilk 10 Creator'ı seçelim
top_creators = combined.sort_values(ascending=False).head(10)
creators = top_creators.index

# Seçilen creator'lar için ilgili sayıların reindex işlemiyle alınması
low_quality_count = low_quality.reindex(creators, fill_value=0).values
medium_quality_count = medium_quality.reindex(creators, fill_value=0).values
high_quality_count = high_quality.reindex(creators, fill_value=0).values

# Toplam JIRA sayılarını elde et ve seçilen creator'lar için reindex yapalım
total_jira = df['Creator'].value_counts()
total_jira_count = total_jira.reindex(creators, fill_value=0).values

# Gruplandırılmış bar grafiği oluşturmak için bar genişliği ve konumlarını ayarlayalım
bar_width = 0.2  # Dört grup olduğu için daha dar genişlik ayarlıyoruz
indices = np.arange(len(creators))

plt.figure(figsize=(12, 6))
plt.bar(indices - 1.5 * bar_width, low_quality_count, width=bar_width, 
        label='Low Kalite JIRA', color='#e74c3c')  # Kırmızı
plt.bar(indices - 0.5 * bar_width, medium_quality_count, width=bar_width, 
        label='Medium JIRA', color='#95a5a6')  # Gri
plt.bar(indices + 0.5 * bar_width, high_quality_count, width=bar_width, 
        label='High JIRA', color='#2ecc71')  # Yeşil (artık üst üste gelmiyor)
plt.bar(indices + 1.5 * bar_width, total_jira_count, width=bar_width, 
        label='Toplam JIRA', color='#3498db')  # Mavi

plt.xlabel('Creator')
plt.ylabel('JIRA Sayısı')
plt.title('Low, Medium, High Kalite JIRA Sayıları ve Toplam JIRA')
plt.xticks(indices, creators, rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()


# CSV olarak dışa aktarma
output_columns = [
    'Key','Creator', 'Jira', 'Description', 'quality', 'score', 'Sorumlu Geliştirici', 
    'quality_score', 'has_acceptance_criteria', 'has_expected_result', 'word_count', 
    'sentence_count', 'avg_word_length', 'has_altsistem', 'has_screenshots', 'url_count', 'Ekran Kodu'
]

# Eğer 'Jira' sütunu yoksa, hata almamak için sütun listesinden çıkarın
output_columns = [col for col in output_columns if col in df.columns]

# CSV dosyasına kaydet
output_file = r'C:\ANALIZ_DATA\jira_analysis_results.csv'
df[output_columns].to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"Dosya başarıyla oluşturuldu: {output_file}")

# Excel dosyası olarak kaydet
df[output_columns].to_excel(r'C:\ANALIZ_DATA\jira_analysis_results.xlsx', index=False, engine='openpyxl')

print("Excel dosyası başarıyla kaydedildi.")