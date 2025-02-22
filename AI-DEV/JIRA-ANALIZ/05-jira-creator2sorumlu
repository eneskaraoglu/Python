import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükleyelim
df = pd.read_csv(r'C:\Users\enesk\Downloads\jira.csv', sep=",", encoding="utf-8")

# Eğer "Sorumlu Geliştirici" sütununda eksik (NaN) veri varsa, ilgili satır için "Creator" değerini kullanalım.
df['Effective Developer'] = df['Sorumlu Geliştirici'].fillna(df['Creator'])

# Effective Developer ile Creator arasındaki ilişkiyi frekans tablosu olarak hesaplayalım.
corr_table = pd.crosstab(df['Effective Developer'], df['Creator'])
print(corr_table)

# Heatmap ile görselleştirme
plt.figure(figsize=(12, 8))
sns.heatmap(corr_table, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Effective Developer (Sorumlu Geliştirici/Creator) ile Creator İlişkisi")
plt.xlabel("Creator")
plt.ylabel("Effective Developer")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()
