import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükleyelim
df = pd.read_csv(r'C:\Users\enesk\Downloads\jira.csv', sep=",", encoding="utf-8")

# "Created" sütununu datetime formatına çevirelim (Türkçe tarih formatına göre, dayfirst=True)
df['Created'] = pd.to_datetime(df['Created'], errors='coerce', dayfirst=True)

# Hafta bazında gruplamak için "Created_Week" sütunu oluşturalım
df['Created_Week'] = df['Created'].dt.to_period('W')

# "Creator" sütununa göre hafta bazında oluşturulan Jira sayısını hesaplayalım
weekly_counts = df.groupby(['Created_Week', 'Creator']).size().reset_index(name='Count')

# Pivot tablo oluşturarak haftaları index, creator'ları sütun olarak düzenleyelim
pivot_weekly = weekly_counts.pivot(index='Created_Week', columns='Creator', values='Count').fillna(0)

# Bar plot ile görselleştirme
plt.figure(figsize=(14, 8))
pivot_weekly.plot(kind='bar')
plt.title("Hafta Bazında Creator'a Göre Açılan Jira Sayısı")
plt.xlabel("Oluşturulma Haftası")
plt.ylabel("Jira Sayısı")
plt.legend(title="Creator", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
