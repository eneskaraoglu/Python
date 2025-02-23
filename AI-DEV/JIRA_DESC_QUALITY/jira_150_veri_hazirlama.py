import pandas as pd

# CSV dosyasını oku. Dosya yolunun başındaki r, raw string olarak işleme alır.
df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv')

# DataFrame'in ilk birkaç satırını görüntüle
print("İlk 5 satır:")
print(df.head())

# Tüm sütun isimlerini listele
print("\nSütun isimleri:")
print(df.columns.tolist())

# Description sütununa ait genel istatistikleri görüntüle
print("\nDescription sütunu istatistikleri:")
print(df['Description'].describe())

# Description sütunundaki boş değerleri kontrol et
print("\nBoş 'Description' değeri sayısı:")
print(df['Description'].isnull().sum())

# Description sütunundaki dolu değerlerin oranını hesapla
print("\nDolu 'Description' oranı:")
print(df['Description'].notnull().mean())
