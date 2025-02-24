import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\ANALIZ_DATA\jira.csv', sep=",", encoding="utf-8")

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

# Issue Tiplerinin dağılımını hesaplama
issue_type_counts = df["Issue Type"].value_counts()

# Issue Tipleri için pie chart
plt.figure(figsize=(8,8))
plt.pie(issue_type_counts, labels=issue_type_counts.index, autopct="%1.1f%%", startangle=140)
plt.title("Issue Tip Dağılımı")
plt.show()


# Proje bazında Status dağılımı hesaplama
project_status = df.groupby('Project')['Status'].value_counts().reset_index(name='Count')
print(project_status)

plt.figure(figsize=(12,8))
sns.barplot(data=project_status, x='Project', y='Count', hue='Status')
plt.title("Proje Bazında Issue Durumu Dağılımı")
plt.xlabel("Proje")
plt.ylabel("Kayıt Sayısı")
plt.xticks(rotation=45)
plt.legend(title="Status")
plt.show()
