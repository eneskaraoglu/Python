import pandas as pd

# Iris veri setini oku
df = pd.read_csv("c:/WORKSPACE/PYTHON/Python/AI-DEV/Basit Veri Analizi ve Görselleştirme/iris.data", header=None)

# İlk birkaç satırı göster
print(df.head())

df.columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]

# İlk birkaç satırı tekrar göster
print(df.head())

# Veri tipi ve eksik değerleri kontrol et
print(df.info())

# Sayısal sütunların istatistiksel özeti
print(df.describe())

# Eksik değer kontrolü
print(df.isnull().sum())

import matplotlib.pyplot as plt
import seaborn as sns

# Histogram çiz
df.hist(figsize=(10, 6), bins=20)
plt.show()

sns.pairplot(df, hue="species")
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Korelasyon Matrisi")
plt.show()