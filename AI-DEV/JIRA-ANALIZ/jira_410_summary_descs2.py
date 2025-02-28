import matplotlib.pyplot as plt

from jira_400_TextAnalysis import TextAnalysis
from wordcloud import WordCloud

if __name__ == "__main__":
    # Özel stopword'lerinizi belirleyin
    custom_words = {'müşteri', 'gamze','çalışmalar'}

    # Sınıfı başlatın; CSV dosya yolunuzu girin
    analysis = TextAnalysis(csv_path=r'C:\ANALIZ_DATA\jira.csv', custom_stopwords=custom_words)

    # Veriyi yükleyin ve ön işlemleri gerçekleştirin
    analysis.load_data()
    analysis.preprocess_text()
    analysis.vectorize_tfidf()

    #analysis.plot_top_words(top_n=20)

    # LDA modelini çalıştırın ve sonuçları yazdırın
    topics = analysis.run_lda(num_topics=50, no_top_words=10)
    for topic, words in topics.items():
        print(f"{topic}: {' '.join(words)}")
        
# TF-IDF sonrası en yüksek skorlu kelimeleri görselleştirin
top_words = analysis.get_top_words(top_n=50)
words, scores = zip(*top_words)
total_score = sum(scores)
percentages = [score / total_score * 100 for score in scores]

# Yatay bar grafik ile görselleştirme
plt.figure(figsize=(10,8))
plt.barh(words[::-1], percentages[::-1], color='skyblue')
plt.xlabel('Yüzde (%)')
plt.title('En Yüksek TF-IDF Skoruna Sahip Kelimeler')
plt.show()
