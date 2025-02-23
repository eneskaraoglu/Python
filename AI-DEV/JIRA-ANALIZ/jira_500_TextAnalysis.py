import nltk
import re
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class TextAnalysis:
    def __init__(self, csv_path, custom_stopwords=None, encoding="utf-8", sep=","):
        """
        csv_path: CSV dosyasının yolu
        custom_stopwords: Eklemek istediğiniz özel stopword'ler (set veya list). Eğer sağlanırsa,
                          varsayılan stopword'ler ile birleşim yapılır.
        encoding: Dosya kodlaması
        sep: CSV ayırıcı karakter
        """
        self.csv_path = csv_path
        self.encoding = encoding
        self.sep = sep
        self.df = None
        self.tfidf_vectorizer = None
        self.tfidf = None
        
        # Varsayılan Türkçe stopword'leri hazırlayalım
        nltk.download('stopwords')
        turkish_stopwords = set(stopwords.words('turkish'))
        
        # Varsayılan custom_stopwords seti
        default_custom_stopwords = {'günlük', 'çalışma_', 'imagepngthumbnail', 'bey', 'hk', 'bir', 
                                    'merhaba', 'ilgili', 'misiniz', 'olarak', 'yapılan'}
        # Eğer kullanıcı kendi custom_stopwords'ünü sağladıysa, varsayılan ile birleşim yapalım.
        if custom_stopwords is None:
            custom_stopwords = default_custom_stopwords
        else:
            custom_stopwords = set(custom_stopwords).union(default_custom_stopwords)
            
        # Son olarak Türkçe stopword'ler ile custom stopword'leri birleştiriyoruz.
        self.combined_stopwords = list(turkish_stopwords.union(custom_stopwords))

    def load_data(self):
        """CSV dosyasını yükler ve 'Summary' ile 'Description' sütunlarını birleştirir."""
        self.df = pd.read_csv(self.csv_path, sep=self.sep, encoding=self.encoding)
        self.df['Text'] = self.df['Summary'].fillna('') + " " + self.df['Description'].fillna('')

    def clean_text(self, text):
        """Metin temizleme fonksiyonu: küçük harf, rakam, noktalama kaldırma ve stopword filtreleme."""
        text = text.lower()
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        tokens = text.split()
        tokens = [word for word in tokens if word not in self.combined_stopwords]
        return ' '.join(tokens)

    def preprocess_text(self):
        """Veri kümesindeki metinleri temizleyip 'Clean_Text' sütununa yazar."""
        if self.df is None:
            self.load_data()
        self.df['Clean_Text'] = self.df['Text'].apply(self.clean_text)

    def vectorize_tfidf(self, max_df=0.95, min_df=2):
        """
        TF-IDF vektörleştirme işlemini gerçekleştirir.
        max_df: Çok yaygın kelimeleri filtrelemek için üst eşik
        min_df: Belirli bir belge sayısının altında geçen kelimeleri filtrelemek için alt eşik
        """
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=self.combined_stopwords, max_df=max_df, min_df=min_df)
        self.tfidf = self.tfidf_vectorizer.fit_transform(self.df['Clean_Text'])

    def get_top_words(self, top_n=20):
        """
        TF-IDF vektörleştirme sonrası en yüksek TF-IDF skoruna sahip kelimeleri döndürür.
        return: (kelime, skor) ikililerinden oluşan liste
        """
        tfidf_feature_names = self.tfidf_vectorizer.get_feature_names_out()
        avg_tfidf = self.tfidf.mean(axis=0).A1
        freq_dict = {word: avg_tfidf[i] for i, word in enumerate(tfidf_feature_names)}
        sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:top_n]

    def plot_top_words(self, top_n=20):
        """En yüksek TF-IDF skoruna sahip kelimeleri yatay bar grafik ile görselleştirir."""
        top_words = self.get_top_words(top_n=top_n)
        words, scores = zip(*top_words)
        total_score = sum(scores)
        percentages = [score / total_score * 100 for score in scores]
        
        plt.figure(figsize=(10, 8))
        plt.barh(words[::-1], percentages[::-1], color='skyblue')
        plt.xlabel('Yüzde (%)')
        plt.title('En Yüksek TF-IDF Skoruna Sahip Kelimeler')
        plt.show()

    def run_lda(self, num_topics=5, no_top_words=10):
        """
        LDA modeli oluşturur ve her konu için en baskın kelimeleri döndürür.
        return: Konu numarası ve ilgili kelimeleri içeren sözlük
        """
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(self.tfidf)
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        topics = {}
        for topic_idx, topic in enumerate(lda.components_):
            top_features_ind = topic.argsort()[:-no_top_words - 1:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            topics[f"Konu {topic_idx + 1}"] = top_features
        return topics
