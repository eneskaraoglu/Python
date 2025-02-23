# Gerekli kütüphaneleri içe aktarıyoruz
import pandas as pd  # Veri manipülasyonu için pandas kütüphanesi
import re  # Regular expressions (düzenli ifadeler) için re kütüphanesi
import nltk  # Doğal dil işleme için NLTK kütüphanesi
from nltk.corpus import stopwords  # NLTK'nin stopwords (etkisiz kelimeler) koleksiyonu
from sklearn.feature_extraction.text import CountVectorizer  # Metin verilerini sayısal matrise dönüştürmek için
from sklearn.decomposition import LatentDirichletAllocation  # Konu modellemesi için LDA algoritması

# NLTK'nin Türkçe stopwords'lerini indiriyoruz
nltk.download('stopwords')

# CSV dosyasını okuyoruz
# sep="," ile virgülle ayrılmış değerleri belirtiyoruz
# encoding="utf-8" ile Türkçe karakterlerin düzgün okunmasını sağlıyoruz
df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv', sep=",", encoding="utf-8")

# Summary ve Description sütunlarını birleştiriyoruz
# fillna('') ile boş değerleri boş string ile dolduruyoruz
# İki sütunu boşluk karakteri ile birleştirip 'Text' adlı yeni bir sütun oluşturuyoruz
df['Text'] = df['Summary'].fillna('') + " " + df['Description'].fillna('')

# Özel olarak belirlediğimiz etkisiz kelimeleri tanımlıyoruz
# Bu kelimeler analiz için önem taşımayan, sık kullanılan kelimelerdir
custom_stopwords = {'günlük', 'çalışma_', 'imagepngthumbnail', 'bey', 'hk', 'bir', 
                   'merhaba', 'ilgili', 'misiniz', 'olarak', 'yapılan'}

# NLTK'nin Türkçe stopwords'lerini bir set olarak alıyoruz
turkish_stopwords = set(stopwords.words('turkish'))

# Özel stopwords'leri ve Türkçe stopwords'leri birleştiriyoruz
all_stopwords = turkish_stopwords.union(custom_stopwords)

# Metin temizleme fonksiyonu
def clean_text(text):
    text = str(text).lower()  # Tüm metni küçük harfe çeviriyoruz ve string'e dönüştürüyoruz
    text = re.sub(r'\d+', '', text)  # Sayıları kaldırıyoruz
    text = re.sub(r'[^\w\s]', '', text)  # Noktalama işaretlerini kaldırıyoruz
    tokens = text.split()  # Metni kelimelere ayırıyoruz
    tokens = [word for word in tokens if word not in all_stopwords]  # Stopwords'leri filtreliyoruz
    return ' '.join(tokens)  # Temizlenmiş kelimeleri tekrar birleştiriyoruz

# Temizleme fonksiyonunu tüm metinlere uyguluyoruz
df['Clean_Text'] = df['Text'].apply(clean_text)

# CountVectorizer ile kelime-doküman matrisini oluşturuyoruz
# max_df=0.95: Kelimelerin en fazla %95'inde görünen kelimeleri ele
# min_df=1: En az 1 dokümanda geçen kelimeleri ele
# stop_words: Daha önce belirlediğimiz stopwords'leri kullanıyoruz
vectorizer = CountVectorizer(max_df=0.95, min_df=1, stop_words=list(all_stopwords))
dtm = vectorizer.fit_transform(df['Clean_Text'])

# LDA modelini oluşturuyoruz
# n_components=num_topics: Kaç farklı konu çıkarmak istediğimizi belirtiyoruz
# random_state=42: Tekrar üretilebilirlik için sabit sayı belirliyoruz
num_topics = 10
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(dtm)  # Modeli eğitiyoruz

# Konuları görüntüleme fonksiyonu
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Konu {topic_idx + 1}: ", end="")
        # Her konu için en önemli kelimeleri sıralıyoruz
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

# Her konu için en önemli no_top_words kelimeyi gösteriyoruz
no_top_words = 3
feature_names = vectorizer.get_feature_names_out()  # Vektörleştirilen kelimelerin listesini alıyoruz
display_topics(lda, feature_names, no_top_words)  # Konuları ve önemli kelimeleri yazdırıyoruz