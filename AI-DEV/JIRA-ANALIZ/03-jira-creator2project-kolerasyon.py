import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükleyelim
df = pd.read_csv(r'C:\Users\enesk\Downloads\jira.csv', sep=",", encoding="utf-8")

# Project ve Creator için frekans tablosu (crosstab) oluşturma
project_creator = pd.crosstab(df['Project'], df['Creator'])
print(project_creator)

# Heatmap ile görselleştirme
plt.figure(figsize=(12, 8))
sns.heatmap(project_creator, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Project ve Creator İlişkisi")
plt.xlabel("Creator")
plt.ylabel("Project")
plt.xticks(rotation=45)
plt.show()
