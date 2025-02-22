import pandas as pd

# CSV dosyanızı okuyun. Eğer dosyanız farklı bir ayırıcı kullanıyorsa sep parametresini güncelleyin.
df = pd.read_csv(r'C:\Users\enesk\Downloads\jira.csv', sep=",", encoding="utf-8")
print(df.head())


# Tarih sütunlarını datetime formatına çevirelim.
date_columns = ["Created", "Last Viewed", "Updated", "Resolved"]  # İhtiyacınıza göre diğer tarih sütunlarını da ekleyin.
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)  # dayfirst=True: Türkçe tarih formatları için

# Eksik verileri kontrol edelim.
print(df.isnull().sum())

# Issue Status dağılımını inceleyelim.
status_counts = df["Status"].value_counts()
print("Issue Durumları:\n", status_counts)

# Issue Type dağılımı
issue_type_counts = df["Issue Type"].value_counts()
print("Issue Tipleri:\n", issue_type_counts)

import matplotlib.pyplot as plt
import seaborn as sns

# Stil ayarları
sns.set(style="whitegrid")

# Issue Durumları için bar plot
plt.figure(figsize=(10,6))
sns.countplot(data=df, x="Status", order=df["Status"].value_counts().index)
plt.title("Issue Durum Dağılımı")
plt.xlabel("Durum")
plt.ylabel("Kayıt Sayısı")
plt.xticks(rotation=45)
plt.show()

# Issue Tipleri için örnek pie chart
plt.figure(figsize=(8,8))
plt.pie(issue_type_counts, labels=issue_type_counts.index, autopct="%1.1f%%", startangle=140)
plt.title("Issue Tip Dağılımı")
plt.show()
