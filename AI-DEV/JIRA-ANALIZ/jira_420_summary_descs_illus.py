import matplotlib.pyplot as plt

from jira_400_TextAnalysis import TextAnalysis
from wordcloud import WordCloud

if __name__ == "__main__":
    # Özel stopword'lerinizi belirleyin
    custom_words = {'müşteri', 'gamze','ekranında'}

    # Sınıfı başlatın; CSV dosya yolunuzu girin
    analysis = TextAnalysis(csv_path=r'C:\ANALIZ_DATA\jira.csv', custom_stopwords=custom_words)

    # Veriyi yükleyin ve ön işlemleri gerçekleştirin
    analysis.load_data()
    analysis.preprocess_text()
    analysis.vectorize_tfidf()
        
# TF-IDF Vektörleştirme
# Kelime frekansları: tfidf vektöründeki ortalama değerleri kullanabiliriz
# get_top_words metodu bir liste döndürüyor, bu yüzden önce sözlüğe çevirelim
top_words_list = analysis.get_top_words(top_n=100)
freq_dict = dict(top_words_list)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(freq_dict)
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("TF-IDF Temelli Anahtar Kelimeler")
plt.show()
