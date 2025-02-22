import pandas as pd

# Iris veri setini oku
df = pd.read_csv("c:/WORKSPACE/PYTHON/Python/AI-DEV/Basit Veri Analizi ve Görselleştirme/adult.data", header=None)

# İlk birkaç satırı göster
print(df.head())

df.columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
]

# Güncellenmiş veri setini görüntüle
print(df.head())

print(df.isnull().sum())  # Eksik değer kontrolü


df.replace("?", pd.NA, inplace=True)

# Eksik değerleri tekrar kontrol et
print(df.isnull().sum())

# Eksik değerleri olan satırları silebiliriz veya doldurabiliriz:
df.dropna(inplace=True)


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8,5))
sns.histplot(df["age"], bins=30, kde=True)
plt.title("Yaş Dağılımı")
plt.show()

plt.figure(figsize=(6,4))
sns.countplot(x=df["income"])
plt.title("Gelir Dağılımı (>50K ve <=50K)")
plt.show()

plt.figure(figsize=(6,4))
sns.countplot(x="sex", hue="income", data=df)
plt.title("Cinsiyete Göre Gelir Dağılımı")
plt.show()

plt.figure(figsize=(10,5))
sns.boxplot(x="income", y="hours_per_week", data=df)
plt.title("Haftalık Çalışma Süresi ve Gelir İlişkisi")
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Sadece sayısal sütunları seçelim
df_numeric = df.select_dtypes(include=["number"])

# Korelasyon matrisi çizelim
plt.figure(figsize=(10,6))
sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Korelasyon Matrisi (Sayısal Değişkenler)")
plt.show()
