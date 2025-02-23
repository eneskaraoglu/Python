import pandas as pd                           # Veri manipülasyonu için pandas kütüphanesi
import re                                     # Düzenli ifadeler (regex) için re kütüphanesi
import nltk                                   # Doğal dil işleme için nltk kütüphanesi
from nltk.corpus import stopwords             # NLTK stopwords (etkisiz kelimeler) koleksiyonu
from sklearn.feature_extraction.text import CountVectorizer  # Metin verilerini sayısal matrise dönüştürmek için
from sklearn.decomposition import LatentDirichletAllocation    # LDA algoritması (konu modelleme) için
import matplotlib.pyplot as plt               # Görselleştirme için matplotlib

# NLTK stopword'leri indiriyoruz (eğer daha önce indirilmediyse)
nltk.download('stopwords')

# CSV dosyasını okuyoruz ve DataFrame'e yüklüyoruz
df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv', sep=",", encoding="utf-8")

# 'Summary' ve 'Description' sütunlarını birleştirip yeni 'Text' sütununu oluşturuyoruz
df['Text'] = df['Summary'].fillna('') + " " + df['Description'].fillna('')

# Özel olarak tanımlanan stopwords'leri belirliyoruz
custom_stopwords = {'günlük', 'çalışma_', 'imagepngthumbnail', 'bey', 'hk', 'bir', 
                    'merhaba', 'ilgili', 'misiniz', 'olarak', 'yapılan'}

# NLTK'nin Türkçe stopwords listesini alıyoruz
turkish_stopwords = set(stopwords.words('turkish'))

# İki stopword kümesini birleştiriyoruz
all_stopwords = turkish_stopwords.union(custom_stopwords)

# Metin temizleme fonksiyonu: Metni küçük harfe çevirir, rakamları ve noktalama işaretlerini kaldırır, stopwords'leri filtreler
def clean_text(text):
    text = str(text).lower()                      # Metni string'e çevirip küçük harfe çeviriyoruz
    text = re.sub(r'\d+', '', text)               # Rakamları kaldırıyoruz
    text = re.sub(r'[^\w\s]', '', text)           # Noktalama işaretlerini kaldırıyoruz
    tokens = text.split()                         # Metni kelimelere ayırıyoruz
    tokens = [word for word in tokens if word not in all_stopwords]  # Stopwords'leri çıkarıyoruz
    return ' '.join(tokens)                       # Temizlenmiş kelimeleri tekrar birleştirip döndürüyoruz

# 'Text' sütunundaki verileri temizleyip 'Clean_Text' sütununa yazıyoruz
df['Clean_Text'] = df['Text'].apply(clean_text)

# "Created" sütunundaki tarih verilerini datetime formatına çeviriyoruz; hatalı veriler NaT olarak işaretlenecektir
df['Created'] = pd.to_datetime(df['Created'], errors='coerce', dayfirst=True)

# Doküman-terim matrisini oluşturmak için CountVectorizer kullanıyoruz, stopwords'leri filtreleyerek
vectorizer = CountVectorizer(max_df=0.95, min_df=1, stop_words=list(all_stopwords))
dtm = vectorizer.fit_transform(df['Clean_Text'])  # Temizlenmiş metinlerden doküman-terim matrisi oluşturuyoruz

# LDA modelini oluşturuyoruz ve 5 konu çıkarmak üzere ayarlıyoruz
num_topics = 5
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(dtm)  # LDA modelini doküman-terim matrisi üzerinden eğitiyoruz

# Her konunun en baskın kelimelerini görüntülemek için fonksiyon tanımlıyoruz
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Konu {topic_idx + 1}: ", end="")  # Konu numarasını yazdırıyoruz
        # Konunun en önemli kelimelerini sıralayıp yazdırıyoruz
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

# Her konu için en önemli 3 kelimeyi görüntülemek istiyoruz
no_top_words = 3
feature_names = vectorizer.get_feature_names_out()  # Vektörleştirilmiş kelimelerin listesini alıyoruz
display_topics(lda, feature_names, no_top_words)      # Konuları ve en önemli kelimeleri yazdırıyoruz

# Her doküman için LDA modelinden konu dağılımlarını elde ediyoruz
topic_distributions = lda.transform(dtm)

# Konu dağılımı DataFrame'ini oluşturuyoruz, sütun adlarını "Topic_1", "Topic_2", ... olarak belirliyoruz
df_topics = pd.DataFrame(topic_distributions, columns=[f"Topic_{i+1}" for i in range(num_topics)])

# Orijinal DataFrame ile konu dağılımı DataFrame'ini sütun bazında birleştiriyoruz
df = pd.concat([df, df_topics], axis=1)

# Zaman serisi analizi için 'Created' sütununu DataFrame'in indexi olarak ayarlıyoruz
df.set_index('Created', inplace=True)

# Resample işlemi ile verileri ayın son günü ('ME' - Month End) bazında grupluyoruz ve sadece sayısal sütunlar üzerinden ortalama hesaplıyoruz
topic_trends = df.resample('ME').mean(numeric_only=True)[[f"Topic_{i+1}" for i in range(num_topics)]]

# Sütun adlarını "Konu 1", "Konu 2", ... şeklinde değiştiriyoruz
topic_trends.columns = [f"Konu {i+1}" for i in range(num_topics)]

# Zaman içinde konuların dağılımını stacked area chart ile görselleştiriyoruz
plt.figure(figsize=(12,8))                 # Grafik boyutunu belirliyoruz
topic_trends.plot.area()                   # Stacked area chart çizdiriyoruz
plt.xlabel("Oluşturulma Tarihi")           # X eksenine etiket ekliyoruz
plt.ylabel("Ortalama Konu Olasılığı")       # Y eksenine etiket ekliyoruz
plt.title("Aylık Konu Dağılımı")             # Grafiğe başlık ekliyoruz
plt.show()                                 # Grafiği ekranda gösteriyoruz
