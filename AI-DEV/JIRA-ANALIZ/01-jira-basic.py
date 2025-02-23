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

