import nltk
nltk.download('stopwords')

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
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
tfidf = tfidf_vectorizer.fit_transform(df['Clean_Text'])

# Örnek: En sık kullanılan anahtar kelimeleri görselleştirmek için word cloud
tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
# Kelime frekansları: tfidf vektöründeki ortalama değerleri kullanabiliriz
avg_tfidf = tfidf.mean(axis=0).A1
freq_dict = {word: avg_tfidf[i] for i, word in enumerate(tfidf_feature_names)}

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dict)
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("TF-IDF Temelli Anahtar Kelimeler")
plt.show()

# LDA ile Topic Modeling
# Öncelikle CountVectorizer kullanarak belgelere kelime sayımı yapalım.
count_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words=stopwords.words('turkish'))
count_data = count_vectorizer.fit_transform(df['Clean_Text'])

# LDA modelini oluşturup eğitelim
num_topics = 5  # Belirlemek istediğiniz konu sayısı
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(count_data)

# Her konunun en baskın kelimelerini yazdıralım
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        top_features_ind = topic.argsort()[:-no_top_words - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        print(f"Konu {topic_idx+1}: {' '.join(top_features)}")

no_top_words = 10
display_topics(lda, count_vectorizer.get_feature_names_out(), no_top_words)
