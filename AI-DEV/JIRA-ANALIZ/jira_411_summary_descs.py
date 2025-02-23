import nltk
from nltk.corpus import stopwords

# Stopwords'leri indirin (eğer daha önce indirilmediyse)
nltk.download('stopwords')

# Mevcut Türkçe stopwords listesini alın
turkish_stopwords = set(stopwords.words('turkish'))

# Eklemek istediğiniz özel kelimeler
custom_words = {'günlük', 'çalışma_', 'imagepngthumbnail', 'bey', 'hk', 'bir','merhaba', 'ilgili','misiniz','olarak','yapılan'}

# İki listeyi birleştirin
combined_stopwords = turkish_stopwords.union(custom_words)

import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# NLTK stopword'leri indir (ilk seferde çalıştırın)
# nltk.download('stopwords')

# Veriyi yükleyelim
df = pd.read_csv(r'C:\Users\enesk\Downloads\jira.csv', sep=",", encoding="utf-8")

# Summary ve Description sütunlarını birleştirelim (opsiyonel, her iki alanı da analiz edebilirsiniz)
df['Text'] = df['Summary'].fillna('') + " " + df['Description'].fillna('')

# Metin temizleme fonksiyonu
def clean_text(text):
    text = text.lower()                                  # Küçük harfe çevir
    text = re.sub(r'\d+', '', text)                      # Rakamları kaldır
    text = re.sub(r'[^\w\s]', '', text)                  # Noktalama işaretlerini kaldır
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords.words('turkish')]
    return ' '.join(tokens)

df['Clean_Text'] = df['Text'].apply(clean_text)

# TF-IDF Vektörleştirme
combined_stopwords = list(turkish_stopwords.union(custom_words))
tfidf_vectorizer = TfidfVectorizer(stop_words=combined_stopwords, max_df=0.95, min_df=2)
tfidf = tfidf_vectorizer.fit_transform(df['Clean_Text'])

# TF-IDF Vektörleştirme işlemi sonrası
tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
avg_tfidf = tfidf.mean(axis=0).A1
freq_dict = {word: avg_tfidf[i] for i, word in enumerate(tfidf_feature_names)}

# En yüksek TF-IDF skoruna sahip ilk 20 kelimeyi seçelim
top_n = 20
sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
top_words = sorted_items[:top_n]
words, scores = zip(*top_words)

# Skorları normalize ederek yüzde değerlerine çevirelim
total_score = sum(scores)
percentages = [score / total_score * 100 for score in scores]

# Yatay bar grafik ile görselleştirme
plt.figure(figsize=(10,8))
plt.barh(words[::-1], percentages[::-1], color='skyblue')
plt.xlabel('Yüzde (%)')
plt.title('En Yüksek TF-IDF Skoruna Sahip Kelimeler')
plt.show()


# LDA modelini oluşturup eğitelim
num_topics = 5  # Belirlemek istediğiniz konu sayısı
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(tfidf)

# Her konunun en baskın kelimelerini yazdıralım
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-no_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        print(f"Konu {topic_idx+1}: {' '.join(top_features)}")

no_top_words = 10
display_topics(lda, tfidf_vectorizer.get_feature_names_out(), no_top_words)
